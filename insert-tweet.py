#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Tweets(db.Model):
    text = db.StringProperty(
                required=True)
    username = db.StringProperty(
                required=True)
    when = db.DateTimeProperty(
                auto_now_add=True)

class APIHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('insert-tweet.html', {}))
        
    def post(self):
        tweet = Tweets(
            text = self.request.get('text'),
            username = self.request.get('username')
        )
        self.response.out.write("Okay");
    
def main():
    app = webapp.WSGIApplication([
        (r'.*', APIHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()
	