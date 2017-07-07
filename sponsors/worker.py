import constants
import logging
import time
import webapp2

from channels.models import Channel
from sponsors.models import Sponsor
from videos.models   import Video

from google.appengine.api import taskqueue

class EnqueueSponsorsFetchTaskHandler (webapp2.RequestHandler):

    def get(self):

        task = taskqueue.add( queue_name = "sponsors-queue",
                              url = "/sponsors/fetcher"
                            )
        self.response.out.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))

class SponsorsFetcherHandler( webapp2.RequestHandler ):

    def post(self):
        logging.info ("Starting to look for sponsors")

        channel = Channel.query(Channel.external_id == constants.BARBARA_CHANNEL_ID).get()

        if channel is None:
            logging.info("Sponsor Fetcher: No channel")
            return

        logging.info("Checking for new sponsors")
        Sponsor.get_sponsors( channel.credentials, channel.external_id )

        if len( Video.query( Video.is_live == True ).fetch()) != 0:
            time.sleep(5)
            task = taskqueue.add( queue_name = "sponsors-queue",
                                  url = "/sponsors/fetcher"
                                )
        logging.info("No longer looking for new Sponsors")

app = webapp2.WSGIApplication([ ('/sponsors/fetcher', SponsorsFetcherHandler),
                                ('/sponsors/enqueue', EnqueueSponsorsFetchTaskHandler)
                              ], debug=True)
