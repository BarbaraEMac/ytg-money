import constants
import httplib2
import json
import logging
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from oauth2client.contrib.appengine import CredentialsNDBProperty
from apiclient.discovery import build

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

    def get_top_live_video_id(self):
        youtube = build(constants.YOUTUBE_API_SERVICE_NAME,
                        constants.YOUTUBE_API_VERSION,
                        http=self.credentials.authorize(httplib2.Http()))

        # Fetch all streams that are currently live
        list_broadcasts_request = youtube.liveBroadcasts().list(
            broadcastStatus = "active",
            part="id,snippet",
            maxResults=50
            )

        top_concurrents = -1
        top_video_id = ""
        # Iterate through them, looking for the one with the most concurrents
        while list_broadcasts_request:
            list_broadcasts_response = list_broadcasts_request.execute()
            broadcasts = list_broadcasts_response.get("items",[])

            if len( broadcasts ) == 0:
                return ""

            # If only 1 broadcast, don't bother doing any more work.
            elif len( broadcasts ) == 1:
                return str(broadcasts[0]["id"])

            for broadcast in broadcasts:

                # Fetch concurrents from the videos API
                videos = youtube.videos().list(part="liveStreamingDetails", id = broadcast["id"]).execute()

                # NOTE: There's a bug if there are N >1 broadcasts and all have 0 viewers
                for video in videos.get("items", []):
                    try:
                        concurrents = video["liveStreamingDetails"]["concurrentViewers"]
                        logging.info("Concurernts %s" % concurrents)

                        if concurrents >= top_concurrents:
                            top_concurrents = concurrents
                            top_video_id = broadcast["id"]
                    except:
                        logging.warning("Exception during concurrents")
                        continue

            list_broadcasts_request = youtube.liveBroadcasts().list_next(
                list_broadcasts_request, list_broadcasts_response)

        return str(top_video_id)
