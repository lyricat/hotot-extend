from google.appengine.ext import db

class Tweets(db.Model):
    name = db.StringProperty(required=True)
    avatar = db.StringProperty(required=True)
    full_text = db.TextProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
