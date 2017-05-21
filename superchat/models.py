import constants
import httplib2
import json
import logging
import os

from viewers import Viewer

from google.appengine.api import users
from google.appengine.ext import ndb
from oauth2client.contrib.appengine import CredentialsNDBProperty
from apiclient.discovery import build

# https://developers.google.com/youtube/v3/live/docs/superChatEvents

class SuperChat(ndb.Model):
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    viewer = ndb.StructuredProperty(viewers.Viewer)

    amount = ndb.FloatProperty()

    currency = ndb.StringProperty()

    usd_amount = ndb.FloatProperty()

    displayString = ndb.StringProperty() # Pretty print for orignial amount+currency

    tier = ndb.IntegerProperty()

    message = ndb.TextProperty()
