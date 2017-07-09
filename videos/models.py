import constants
import helpers

import logging

from datetime import datetime
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

class Video(ndb.Model):
    # Added this object was created
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    channel_id = ndb.StringProperty(indexed=True)

    title = ndb.StringProperty()

    video_id = ndb.StringProperty(indexed=True)

    start_time = ndb.DateTimeProperty()

    end_time = ndb.DateTimeProperty()

    is_live = ndb.BooleanProperty(default=False)

    def _post_put_hook(self, future):
        logging.info("VIDEO WAS JUST SAVED: %s %s" %(self.video_id, self.is_live))

        # If we have a new LIVE video, start fetching things quickly
        if self.is_live:
            if not memcache.replace( key="BARBARA_IS_LIVE", value=True ):
                memcache.add( key="BARBARA_IS_LIVE", value=True)

            logging.info("Starting to fetch Sponsor now")
            task = taskqueue.add( queue_name = "sponsors-queue",
                                   url = "/sponsors/fetcher"
                                 )
            logging.info("Starting to fetch Super Chats now")
            task = taskqueue.add( queue_name = "superchats-queue",
                                   url = "/superchats/fetcher"
                                 )
            logging.info("Starting to fetch Subscribers now")
            task = taskqueue.add( queue_name = "subscribers-queue",
                                   url = "/subscribers/fetcher"
                                 )

        # Otherwise, turn everything off!
        else:
            memcache.replace( key="BARBARA_IS_LIVE", value=False )

            q = taskqueue.Queue( "sponsors-queue" )
            q.purge()
            q = taskqueue.Queue( "superchats-queue" )
            q.purge()
            q = taskqueue.Queue( "subscribers-queue" )
            q.purge()


    @staticmethod
    def get_and_save_live_videos( credentials ):
        logging.info("Video.get_and_save_live_videos START")

        youtube = helpers.auth_http( credentials )

        # Fetch all streams that are currently live
        logging.info("get_and_save_live_videos: Fetching all live streams")
        list_broadcasts_request = youtube.liveBroadcasts().list(
            broadcastStatus = "active",
            broadcastType="all",
            part="id,snippet",
            maxResults=50
            )

        formerly_live = None
        if helpers.is_barbara_live():
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
        if formerly_live is not None:
            for stream in formerly_live:
                if stream.video_id not in live_ids:
                    logging.info("get_and_save_live_videos: %s is no longer live" % stream.video_id)
                    stream.is_live = False
                    stream.end_time = datetime.now()
                    stream.put()

    @staticmethod
    def get_top_live_video_id( credentials ):

        # Fetch all new live videos
        Video.get_and_save_live_videos( credentials )

        live_videos = Video.query( Video.is_live == True ).fetch()

        if len(live_videos) is 0:
            return ""

        youtube = helpers.auth_http( credentials )

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
