#!/usr/bin/env python

#Default imports
import wsgiref.handlers
import string
import random
import json
import urlparse
import model

#Google App Engine imports
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

def insertDB(tmp_text, tmp_name, tmp_avatar):
    tweet = model.Tweets(name=tmp_name, avatar=tmp_avatar,full_text=tmp_text)
    return tweet.put()


class APIHandler(webapp.RequestHandler):
    ERROR = {
        "result": "error",
        "error": "error_no_direct_connection"
    }
    ID_OFFSET = 100
    SEPERATOR = ' (...) '
    SEPERATOR_LEN = 7
    def get(self):
        self.response.out.write(json.dumps(self.ERROR))

    def post(self):
        #maximum characters for twitter
        maxlen = 140

        text = self.request.get("text")
        name = self.request.get("name")
        avatar = self.request.get("avatar")
        # check form values
        # @TODO erro handle
        if not (text and avatar and name):
            return
        if len(text) > 10240 or len(name) > 32 or len(avatar) > 1024:
            return
        key = insertDB(text, name, avatar)

        url = 'http://hotot.in/' + str(self.ID_OFFSET + key.id())
        maxlen -= len(url) + self.SEPERATOR_LEN
        sliced_text = text[0:maxlen] + self.SEPERATOR + url

        #create an array to convert it to json and give it back to the user
        respond = {
                'id': key.id(),
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

