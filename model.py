from google.appengine.ext import db

class Tweets(db.Model):
    name = db.StringProperty(required=True)
    avatar = db.StringProperty(required=True)
    full_text = db.StringProperty(multiline=True,required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    orig_link = db.StringProperty(required=True)
