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

# https://developers.google.com/youtube/v3/live/docs/sponsors

class Sponsor(ndb.Model):
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    sponsor_since = ndb.DateTimeProperty()

    is_active = nbd.BooleanProperty(default=True)

    viewer = ndb.StructuredProperty(viewers.Viewer)
