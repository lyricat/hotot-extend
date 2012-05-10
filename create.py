#!/usr/bin/env python

#Default imports
import wsgiref.handlers
import string
import random
import urlparse

#django imports
from django.utils import simplejson

#Google App Engine imports
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

def id_generator(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
    
def getUniqueTextID():
    text_id = id_generator();
    result = db.GqlQuery("SELECT * FROM Tweets WHERE text_id = :textid", text_id)
    while True:
	if hasattr(result, 'text_id'):
	    text_id = id_generator()
	else:
	    return text_id

def insertDB(tmp_text):
    if tmp_text != None:
	tmp_id = getUniqueTextID()
	tweet = Tweets(text_id=tmp_id,full_text=tmp_text)
	tweet.put()
	return tmp_id

class Tweets(db.Model):
    text_id = db.StringProperty(required=True)
    full_text = db.StringProperty(multiline=True,required=True)
    date = db.DateTimeProperty(auto_now_add=True)

class APIHandler(webapp.RequestHandler):
    def get(self):
	error = {
	    "result": "error",
	    "error": "error_no_direct_connection"
	}
	
	#create json_encoder
	json_encoder = simplejson.encoder.JSONEncoder()
	
        self.response.out.write(json_encoder.encode(error))
        
    def post(self):
	#maximum characters for twitter
	maxlen = 140
	
	#insertDB will insert the text and the text_id into the database and return the text_id. A unique one
	tweettext = self.request.get("text")
	text_id = insertDB(tweettext)
	
	#base_url contains everything about the host url
	base_url = urlparse.urlparse(self.request.url)
	    
	#build our URL with the text_id behind
	url = 'http://hotot.in/' + text_id
	
	#the seperator
	seperator = ' (...) '
	
	#this is the url length in characters
	url_len = len(url)
	
	#this is the length of the seperator
	sep_len = len(seperator)
	
	#substrate the url_len from the maxlen object to get the maximum text length
	maxlen = maxlen - url_len
	maxlen = maxlen - sep_len
	
	#this is the new twitter string reduced to 140 characters with the url
	sliced_text = tweettext[0:maxlen]
	
	#append the url
	sliced_text = sliced_text + seperator + url
	
	#create an array to convert it to json and give it back to the user
	respond = {
	    'id': text_id,
	    'url': url,
	    'full_text': tweettext,
	    'text': sliced_text
	}
	
	#create json_encoder
	json_encoder = simplejson.encoder.JSONEncoder()
	
	#print out the json string to the user
        self.response.out.write(json_encoder.encode(respond))
    
def main():
    app = webapp.WSGIApplication([
        (r'.*', APIHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()
	