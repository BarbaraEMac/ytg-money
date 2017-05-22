import constants
import logging
import time
import webapp2

from channels.models import Channel
from sponsors.models import Sponsor

from google.appengine.api import taskqueue

class EnqueueSponsorsFetchTaskHandler (webapp2.RequestHandler):

    def get(self):

        task = taskqueue.add( queue_name = "sponsors-queue",
                              url = "/sponsors/fetcher"
                            )
        self.response.out.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))

class SponsorsFetcherHandler( webapp2.RequestHandler ):

    def post(self):
        channel = Channel.query(Channel.external_id == constants.BARBARA_CHANNEL_ID).get()

        if channel is None:
            logging.info("Video Fetcher: No channel")
            return

        logging.info("Checking for new sponsors")
        Sponsor.get_sponsors( channel.credentials, channel.external_id )

        # Now, enqueue the next task
        time.sleep(1)
        task = taskqueue.add( queue_name = "sponsors-queue",
                              url = "/sponsors/fetcher"
                            )

app = webapp2.WSGIApplication([ ('/sponsors/fetcher', SponsorsFetcherHandler),
                                ('/sponsors/enqueue', EnqueueSponsorsFetchTaskHandler)
                              ], debug=True)
