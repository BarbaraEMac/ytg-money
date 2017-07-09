import constants
import helpers
import logging
import time
import webapp2

from channels.models import Channel
from subscribers.models import Subscriber
from videos.models   import Video

from google.appengine.api import taskqueue

class EnqueueSubsFetchTaskHandler (webapp2.RequestHandler):

    def get(self):

        task = taskqueue.add( queue_name = "subscribers-queue",
                              url = "/subscribers/fetcher"
                            )
        self.response.out.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))

class SubsFetcherHandler( webapp2.RequestHandler ):

    def post(self):
        logging.info ("Starting to look for subs")

        channel_creds= Channel.get_barbara_creds()

        if channel_creds is None:
            logging.info("Sponsor Fetcher: No channel")
            return

        logging.info("Checking for new subs")
        Subscriber.get_subs( channel_creds, constants.BARBARA_CHANNEL_ID )

        if helpers.is_barbara_live():
            #time.sleep(5)
            task = taskqueue.add( queue_name = "subscribers-queue",
                                  url = "/subscribers/fetcher"
                                )
        logging.info("No longer looking for new subs")

app = webapp2.WSGIApplication([ ('/subscribers/fetcher', SubsFetcherHandler),
                                ('/subscribers/enqueue', EnqueueSubsFetchTaskHandler)
                              ], debug=True)
