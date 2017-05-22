import constants
import httplib2
import json
import logging
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from oauth2client.contrib.appengine import CredentialsNDBProperty
from apiclient.discovery import build

class Video(ndb.Model):
    # Added this object was created
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    channel_id = ndb.StringProperty(indexed=True)

    title = ndb.StringProperty()

    video_id = ndb.StringProperty(indexed=True)

    start_time = ndb.DateTimeProperty()

    end_time = ndb.DateTimeProperty()

    is_live = ndb.BooleanProperty(default=False)
