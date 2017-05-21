import constants
import httplib2
import json
import logging
import os

from videos import Video

from google.appengine.api import users
from google.appengine.ext import ndb
from oauth2client.contrib.appengine import CredentialsNDBProperty
from apiclient.discovery import build

class Viewer(ndb.Model):
    # Added this object was created
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    # YouTube channel id
    external_id = ndb.StringProperty(default="", indexed=True)

    # YouTube channel url
    channel_url = ndb.StringProperty(default="", indexed=True)

    # Channel's display name
    name = ndb.StringProperty(default="", indexed=False)

    # Profile image URL
    image = ndb.StringProperty()

    num_streams = ndb.IntegerProperty()

    first_stream = ndb.StructuredProperty(videos.Video)
    most_recent_stream = ndb.StructuredProperty(videos.Video)

    all_streams = ndb.StructuredProperty(videos.Video, repeated=True)

    super_chat_total = ndb.FloatProperty()

    is_sponsor = ndb.BooleanProperty(default=False)
