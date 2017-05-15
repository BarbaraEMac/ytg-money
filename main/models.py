import cgi
import urllib

from google.appengine.ext import ndb
from google.appengine.api import users

import webapp2

class Alert(ndb.Model):
    time = ndb.DateTimeProperty(auto_now_add=True)
    delivered = ndb.BooleanProperty(default=False, indexed=True)
    test = ndb.BooleanProperty(default=False, indexed=False)

    user_id = ndb.StringProperty(default="", indexed=True)
    name = ndb.StringProperty(default="", indexed=False)
    image = ndb.StringProperty(default="", indexed=False)
    text = ndb.StringProperty(default="", indexed=False)
    amount = ndb.IntegerProperty(default=0, indexed=False)
    sponsor = ndb.BooleanProperty(default=False, indexed=True)

class LastActivity(ndb.Model):
    user = ndb.KeyProperty()
    timestamp = ndb.DateTimeProperty()

class Updater(ndb.Model):
    last_update = ndb.DateTimeProperty()
    next_update = ndb.DateTimeProperty()
    last_failure = ndb.DateTimeProperty()
    last_failure_message = ndb.StringProperty(default="")
    failure_count = ndb.IntegerProperty(default=0)
    user = ndb.KeyProperty()
    running = ndb.BooleanProperty(default=False)

class UpdaterEvent(ndb.Model):
    external_id = ndb.StringProperty(default="", indexed=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    base_updater = ndb.KeyProperty(kind=Updater)
