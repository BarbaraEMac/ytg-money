import constants
import httplib2
import json
import logging
import os

from videos.models import Video

from apiclient.discovery import build
from datetime import datetime
from google.appengine.api import users
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

    def get_and_save_live_videos(self):
        logging.info("Channel.get_and_save_live_videos START")

        youtube = build(constants.YOUTUBE_API_SERVICE_NAME,
                        constants.YOUTUBE_API_VERSION,
                        http=self.credentials.authorize(httplib2.Http()))

        # Fetch all streams that are currently live
        logging.info("get_and_save_live_videos: Fetching all live streams")
        list_broadcasts_request = youtube.liveBroadcasts().list(
            broadcastStatus = "active",
            part="id,snippet",
            maxResults=50
            )

        formerly_live = Video.query( Video.is_live == True ).fetch()

        live_ids = []
        while list_broadcasts_request:
            list_broadcasts_response = list_broadcasts_request.execute()
            broadcasts = list_broadcasts_response.get("items",[])

            for broadcast in broadcasts:
                logging.info("get_and_save_live_videos: Iterating over broadcasts")

                video_id = broadcast["id"]
                live_ids.append(video_id)

                video = Video.query( Video.video_id == video_id ).get()

                if video is None:
                    # If we don't have this video in the DB, make on

                    start_time = datetime.strptime( broadcast["snippet"]["actualStartTime"], "%Y-%m-%dT%H:%M:%S.%fZ" )

                    video = Video( title = broadcast["snippet"]["title"],
                                   channel_id = broadcast["snippet"]["channelId"],
                                   video_id = video_id,
                                   start_time = start_time,
                                   is_live = True
                                )

                    logging.info("get_and_save_live_videos: Saving 1 live video: %s" % video_id)
                    video.put()
                    # end for

            list_broadcasts_request = youtube.liveBroadcasts().list_next(
                list_broadcasts_request, list_broadcasts_response)
            # end while

        # Go through formerly live videos.
        # If we didn't fetch it now, it must be over.
        for stream in formerly_live:
            if stream.video_id not in live_ids:
                logging.info("get_and_save_live_videos: %s is no longer live" % stream.video_id)
                stream.is_live = False
                stream.end_time = datetime.now()
                stream.put()


    def get_top_live_video_id(self):

        # Fetch all new live videos
        self.get_and_save_live_videos()

        live_videos = Video.query( Video.is_live == True ).fetch()

        if len(live_videos) is 0:
            return ""

        youtube = build(constants.YOUTUBE_API_SERVICE_NAME,
                        constants.YOUTUBE_API_VERSION,
                        http=self.credentials.authorize(httplib2.Http()))

        top_concurrents = 0
        top_video_id = live_videos[0].video_id
        for live_video in live_videos:

            # Fetch concurrents from the videos API
            videos = youtube.videos().list(part="liveStreamingDetails", id = live_video.video_id).execute()

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

        return str(top_video_id)
