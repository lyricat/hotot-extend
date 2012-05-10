#!/usr/bin/env python

#Default imports
import wsgiref.handlers
import json
import string
import random
import urlparse

#Google App Engine imports
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

def id_generator(size=6, chars=string.ascii_letters + string.digits):
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
        self.response.out.write(json.dumps(['error', 'error_direct_connection']))
        
    def post(self):
	#maximum characters for twitter
	maxlen = 140
	
	#insertDB will insert the text and the text_id into the database and return the text_id. A unique one
	tweettext = self.request.get("text")
	text_id = insertDB(tweettext)
	
	#base_url contains everything about the host url
	base_url = urlparse.urlparse(self.request.url)
	#check if the port of the host isn't 80. If so we have to add it after the hostname
	if(base_url.port != 80):
	    port = ':{0}'.format(base_url.port)
	else:
	    port = ''
	    
	#build our URL with the text_id behind
	url = ' (...) http://' + base_url.hostname + port + '/' + text_id
	
	#this is the url length in characters
	url_len = len(url)
	
	#substrate the url_len from the maxlen object to get the maximum text length
	maxlen = maxlen - url_len
	
	#this is the new twitter string reduced to 140 characters with the url
	sliced_text = tweettext[0:maxlen]
	
	#append the url
	sliced_text = sliced_text + url
	
	#create an array to convert it to json and give it back to the user
	respond = {
	    'id': text_id,
	    'url': url,
	    'full_text': tweettext,
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
	