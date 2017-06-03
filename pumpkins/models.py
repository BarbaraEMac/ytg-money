from google.appengine.ext import ndb

class Pumpkin(ndb.Model):
    id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    amount = ndb.IntegerProperty()
    profile_URL = ndb.StringProperty()
    x_position = ndb.FloatProperty()
    y_position = ndb.FloatProperty()
    rotation = ndb.FloatProperty()
