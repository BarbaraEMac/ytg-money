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

# https://developers.google.com/youtube/v3/live/docs/superChatEvents

class SuperChat(ndb.Model):
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    created_at  = ndb.DateTimeProperty()

    id = ndb.StringProperty(indexed=True)

    owner_channel_id = ndb.StringProperty()

    viewer = ndb.StructuredProperty(Viewer)

    amount_micros = ndb.IntegerProperty(default=0)

    currency = ndb.StringProperty()

    usd_amount = ndb.FloatProperty(default=0)

    display_string = ndb.StringProperty() # Pretty print for orignial amount+currency

    tier = ndb.IntegerProperty()

    text  = ndb.TextProperty()

    @staticmethod
    def get_superchats( credentials, requesting_channel_id ):
        return 

        youtube = helpers.auth_http( credentials )

        request = youtube.superChatEvents().list( part="id,snippet",
                                           maxResults=50 )

        while request:
            # Fetch first batch of 50
            response = request.execute()
            superchats = response["items"]

            logging.info("GETSUPERCHATS: %i" % len(superchats))
            if len(superchats) == 0:
                return

            for superchat_obj in superchats:
                id = superchat_obj["id"]
                superchat = superchat_obj["snippet"]

                owner_channel_id = superchat['channelId']

                channel_id = superchat['supporterDetails']['channelId']
                channel_url = superchat['supporterDetails']['channelUrl']
                name = superchat['supporterDetails']['displayName']
                image = superchat['supporterDetails']['profileImageUrl']

                text = superchat['commentText']
                created_at = datetime.strptime( superchat["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ" )
                amountMicros = int( superchat['amountMicros'] )
                currency = superchat['currency']
                usd_amount = helpers.convert_to_usd( amountMicros, currency )
                displayString = superchat['displayString']
                tier = superchat['messageType']

                sc = SuperChat.query( SuperChat.id == id ).get()

                # If we've already saved this one, keep going
                if sc:
                    continue

                # Otherwise, get the viewer corresponding to this user
                viewer = Viewer.query( Viewer.channel_id == channel_id ).get()

                # Make a vew Viewer if we don't have one
                if viewer is None:
                    viewer = Viewer( channel_id = channel_id,
                                     channel_url = channel_url,
                                     name = name,
                                     image = image
                                   )
                if viewer.super_chat_total is not None:
                    viewer.super_chat_total = viewer.super_chat_total + usd_amount
                else:
                    viewer.super_chat_total = usd_amount
                viewer.put()

                # Now, make the new superchat and save it
                sc = SuperChat( owner_channel_id = owner_channel_id,
                                viewer           = viewer,
                                id = id,
                                text = text,
                                created_at = created_at,
                                amount_micros = amountMicros,
                                usd_amount = usd_amount,
                                currency = currency,
                                display_string = displayString,
                                tier = tier )
                sc.put()

                Alert.create_superchat_alert( viewer, text, usd_amount )
                # end for

            request = youtube.superChatEvents().list_next( request, response )
            # end while
