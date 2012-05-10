#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class APIHandler(webapp.RequestHandler):
    def get(self):
        tweets = db.GqlQuery('SELECT * FROM Tweets ORDER BY when DESC')
        values = {
            'tweets': tweets
        }
        self.response.out.write(template.render('main.html', values))

def main():
    app = webapp.WSGIApplication([
        (r'.*', APIHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()