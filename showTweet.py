#standart imports
import urlparse
import wsgiref.handlers
import string

#google imports
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class TweetHandler(webapp.RequestHandler):
    def get(self):
        base_url = urlparse.urlparse(self.request.url)
        if hasattr(base_url, "path"):
            if base_url.path.replace('/','') != None:
                text_id = base_url.path.replace('/','')

def main():
    app = webapp.WSGIApplication([
        (r'.*', TweetHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()