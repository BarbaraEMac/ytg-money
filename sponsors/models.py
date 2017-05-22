import constants
import helpers
import logging

from viewers.models import Viewer

from datetime import datetime
from google.appengine.ext import ndb

# https://developers.google.com/youtube/v3/live/docs/sponsors

class Sponsor(ndb.Model):
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    sponsored_channel_id = ndb.StringProperty()

    sponsor_since = ndb.DateTimeProperty()

    cancelled_date = ndb.DateTimeProperty()

    is_active = ndb.BooleanProperty(default=True)

    viewer = ndb.StructuredProperty(Viewer)

    @staticmethod
    def get_sponsors( credentials ):
        youtube = helpers.auth_http( credentials )

        request = youtube.sponsors().list( part="id,snippet",
                                           filter="all",
                                           maxResults=50 )
        while request:
            # Fetch first batch of 50
            response = request.execute()
            sponsors = response["items"]

            logging.info("GETSPONSOR: %i" % len(sponsors))
            if len(sponsors) == 0:
                return

            for sponsor_obj in sponsors:
                sponsor = sponsor_obj["snippet"]

                sponsored_channel_id = sponsor['channelId']
                channel_id = sponsor['sponsorDetails']['channelId']
                channel_url = sponsor['sponsorDetails']['channelUrl']
                name = sponsor['sponsorDetails']['displayName']
                image = sponsor['sponsorDetails']['profileImageUrl']
                sponsor_since = datetime.strptime( sponsor["sponsorSince"], "%Y-%m-%dT%H:%M:%S.%fZ" )

                spn = Sponsor.query( Sponsor.viewer.channel_id == channel_id ).get()

                # If we've already saved this one, keep going
                if spn:
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

                viewer.is_sponsor = True
                viewer.put()

                # Now, make the new Sponsor and save it
                spn = Sponsor( sponsored_channel_id = sponsored_channel_id,
                               sponsor_since = sponsor_since,
                               is_active = True,
                               viewer = viewer )
                spn.put()
                # end for

            request = youtube.sponsors().list_next( request, response )
            # end while

