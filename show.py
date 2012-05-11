#standart imports
import urlparse
import wsgiref.handlers
import string

#google imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.db import Key

import model

class TweetHandler(webapp.RequestHandler):
    def get(self):
        base_url = urlparse.urlparse(self.request.url)
        if base_url.path:
            try:
                id = int(base_url.path[1:])
            except :
                # @TODO need an error handler
                self.response.out.write('error')
                return
            if id:
                try:
                    result = model.Tweets.get_by_id(id - 100)
                except:
                    # @TODO need an error handler
                    self.response.out.write('error')
                    return
                if result:
                    r = template.render('show.html', 
                        {'tweet': result})
                    self.response.out.write(str(r.encode('utf-8')))
                else:
                    # @TODO need an error handler
                    tweet = {
                        'full_text': "The text you are looking for does not exist!"
                    }
                    values = {
                        'tweet': tweet
                    }
                    self.response.out.write(
                        template.render('show.html', values)
                    )
                    
def main():
    app = webapp.WSGIApplication([
        (r'.*', TweetHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()
