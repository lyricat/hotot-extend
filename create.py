#!/usr/bin/env python

#Default imports
import wsgiref.handlers
import string
import random
import json
import urlparse

#Google App Engine imports
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

def id_generator(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def getUniqueTextID():
    whilecount = 0
    text_id = id_generator()
    result = db.GqlQuery("SELECT * FROM Tweets WHERE text_id = :1", text_id)
    while True:
        whilecount = whilecount + 1
        if hasattr(result, "text_id"):
            text_id = id_generator()
        else:
            return text_id
        
        if whilecount == 10:
            return error
            break

def insertDB(tmp_text,tmp_name,tmp_avatar):
    tmp_id = getUniqueTextID()
    tweet = Tweets(text_id=tmp_id,name=tmp_name,avatar=tmp_avatar,full_text=tmp_text)
    tweet.put()
    return tmp_id

class Tweets(db.Model):
    text_id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    avatar = db.StringProperty(required=True)
    full_text = db.StringProperty(multiline=True,required=True)
    date = db.DateTimeProperty(auto_now_add=True)

class APIHandler(webapp.RequestHandler):
    def get(self):
        error = {
                "result": "error",
                "error": "error_no_direct_connection"
                }
        self.response.out.write(json.dumps(error))

    def post(self):
        #maximum characters for twitter
        maxlen = 140
        #insertDB will insert the text and the text_id into the database and return the text_id. A unique one
        text = self.request.get("text")
        name = self.request.get("name")
        avatar = self.request.get("avatar")
        text_id = insertDB(text, name, avatar)
        #build our URL with the text_id behind
        url = 'http://hotot.in/' + text_id
        #the seperator
        seperator = ' (...) '
        #substrate the url_len from the maxlen object to get the maximum text length
        maxlen -= len(url) + len(seperator)
        #this is the new twitter string reduced to 140 characters with the url
        sliced_text = text[0:maxlen] + seperator + url
        #create an array to convert it to json and give it back to the user
        respond = {
                'id': text_id,
                'url': url,
                'full_text': text,
                'text': sliced_text
                }

        #print out the json string to the user
        self.response.out.write(json.dumps(respond))

def main():
    app = webapp.WSGIApplication([
        (r'.*', APIHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()

