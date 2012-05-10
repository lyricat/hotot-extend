#standart imports
import urlparse
import wsgiref.handlers
import string

#google imports
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Tweets(db.Model):
    text_id = db.StringProperty(required=True)
    full_text = db.StringProperty(multiline=True,required=True)
    date = db.DateTimeProperty(auto_now_add=True)

class TweetHandler(webapp.RequestHandler):
    def get(self):
        base_url = urlparse.urlparse(self.request.url)
        if hasattr(base_url, "path"):
            if base_url.path.replace('/','') != None:
                text_id = base_url.path.replace('/','')
                
                result = db.GqlQuery("SELECT * FROM Tweets WHERE text_id = :1", text_id)
                
                for tweet in result:
                    if hasattr(tweet, "full_text"):
                        values = {
                            'tweet': tweet
                        }
                        self.response.out.write(template.render('showTweet.html', values))
                    else:
                        break
                    

def main():
    app = webapp.WSGIApplication([
        (r'.*', TweetHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()