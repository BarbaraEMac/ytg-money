import constants
import helpers
import logging
import time
import webapp2

from channels.models import Channel
from sponsors.models import Sponsor
from videos.models   import Video

from google.appengine.api import taskqueue

class EnqueueSponsorsFetchTaskHandler (webapp2.RequestHandler):

    def get(self):
        return

        task = taskqueue.add( queue_name = "sponsors-queue",
                              url = "/sponsors/fetcher"
                            )
        self.response.out.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))

class SponsorsFetcherHandler( webapp2.RequestHandler ):

    def post(self):
        logging.info ("Starting to look for sponsors")

        channel_creds= Channel.get_barbara_creds()

        if channel_creds is None:
            logging.info("Sponsor Fetcher: No channel")
            return

        logging.info("Checking for new sponsors")
        Sponsor.get_sponsors( channel_creds, constants.BARBARA_CHANNEL_ID )

        if helpers.is_barbara_live():
            #time.sleep(5)
            task = taskqueue.add( queue_name = "sponsors-queue",
                                  url = "/sponsors/fetcher"
                                )
        logging.info("No longer looking for new Sponsors")

app = webapp2.WSGIApplication([ ('/sponsors/fetcher', SponsorsFetcherHandler),
                                ('/sponsors/enqueue', EnqueueSponsorsFetchTaskHandler)
                              ], debug=True)
