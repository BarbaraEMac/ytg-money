import constants
import httplib2
import json
import logging
import os

from apiclient.discovery import build
from datetime import datetime
from google.appengine.api import memcache, users
from google.appengine.ext import ndb
from oauth2client.contrib.appengine import CredentialsNDBProperty

class Channel(ndb.Model):
    # Added this object was created
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    # Oauth crednetials for auth'ing http requests
    credentials = CredentialsNDBProperty()

    # Json for aOauth crednetials for auth'ing http requests
    credentials_json = ndb.JsonProperty()

    # google's unique identifier for the Users service
    user_id = ndb.StringProperty()

    # YouTube channel id
    external_id = ndb.StringProperty(default="", indexed=True)

    # Channel's display name
    name = ndb.StringProperty(default="", indexed=False)

    # Email address
    email = ndb.StringProperty()

    @classmethod
    def _pre_put_hook(self):
        logging.info("Saving a new Channel: %s" % self.external_id)

    @classmethod
    def _pre_get_hook(self):
        logging.info("Fetching Channel: %s" % self.external_id)

    @staticmethod
    def get_or_create( credentials, user ):

        youtube = build(constants.YOUTUBE_API_SERVICE_NAME,
                        constants.YOUTUBE_API_VERSION,
                        http=credentials.authorize(httplib2.Http()))

        channel_details = youtube.channels().list(mine=True, part='id, snippet').execute()
        external_id = channel_details['items'][0]['id']
        name = channel_details['items'][0]['snippet']['title']

        channel = Channel.query(Channel.external_id == external_id).get()

        if channel is None:
            channel = Channel(credentials = credentials,
                              credentials_json = credentials.to_json(),
                              external_id = external_id,
                              name = name,
                              user_id = user.user_id(),
                              email = user.email())
            channel.put()

        return channel

    @staticmethod
    def get_barbara_creds():
        creds = memcache.get(key="BARBARA_CREDS")

        if creds is None:
            channel = Channel.query(Channel.external_id == constants.BARBARA_CHANNEL_ID).get()

            if channel is not None:
                creds = channel.credentials
                memcache.add(key="BARBARA_CREDS", value=creds)

        return creds
