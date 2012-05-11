#standart imports
import urlparse
import wsgiref.handlers
import string

#google imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.db import Key
from google.appengine.api import memcache

import model

class TweetHandler(webapp.RequestHandler):
    def get(self):
        base_url = urlparse.urlparse(self.request.url)
        if base_url.path:
            id_str = base_url.path[1:]
            r = memcache.get(id_str)
            if r is None:
                try:
                    id = int(id_str)
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
                        result.id = id
                        r = str(template.render('show.html', 
                            {'tweet': result}).encode('utf-8'))
                        memcache.set(id_str, r)
                        self.response.out.write(r)
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
            else:
                self.response.out.write(r)

                    
def main():
    app = webapp.WSGIApplication([
        (r'.*', TweetHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()
