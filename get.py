#standart imports
import urlparse
import wsgiref.handlers
import string
import json

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
            id_json = base_url.path[7:]
            id_len = len(id_json) - 5
            id_str = id_json[0:id_len]
            r = memcache.get(id_json)
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
                        response = {
                            'id': result.id,
                            'url': "http://hotot.in/" + id_str,
                            'full_text': result.full_text
                        }
                        r = json.dumps(response)
                        memcache.set(id_json, r)
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
