import constants
import httplib2
import json
import logging
import os

import helpers

from alerts.models import Alert
from viewers.models import Viewer

from datetime import datetime
from google.appengine.ext import ndb
from apiclient.discovery import build

# https://developers.google.com/youtube/v3/live/docs/subEvents

class Subscriber(ndb.Model):

    @staticmethod
    def get_subs( credentials, requesting_channel_id ):

        youtube = helpers.auth_http( credentials )

        request = youtube.subscriptions().list( part="subscriberSnippet",
                                                myRecentSubscribers="true",
                                                maxResults=25 )

        while request:
            # Fetch first batch of 25
            response = request.execute()
            subs = response["items"]

            logging.info("GETSUBS: %i" % len(subs))
            if len(subs) == 0:
                return

            for sub_obj in subs:
                sub = sub_obj["subscriberSnippet"]

                channel_id = sub['channelId']
                name = sub['title']
                image = str( sub['thumbnails']['default'] )

                viewer = Viewer.query( Viewer.channel_id == channel_id ).get()

                # If we've already saved this one, keep going
                if viewer:
                    if not viewer.is_sub:
                        viewer.is_sub = True
                        viewer.put()

                    continue

                # Make a vew Viewer if we don't have one
                if viewer is None:
                    viewer = Viewer( channel_id = channel_id,
                                     name = name,
                                     image = image,
                                     is_sub = True
                                   )
                viewer.put()

                Alert.create_sub_alert( viewer )
                # end for

            request = youtube.subscriptions().list_next( request, response )
            # end while
