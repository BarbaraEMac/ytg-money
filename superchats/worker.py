import constants
import helpers
import logging
import time
import webapp2

from channels.models import Channel
from superchats.models import SuperChat
from videos.models   import Video

from google.appengine.api import taskqueue

class EnqueueSuperChatsFetchTaskHandler (webapp2.RequestHandler):

    def get(self):
        return 

        task = taskqueue.add( queue_name = "superchats-queue",
                              url = "/superchats/fetcher"
                            )
        self.response.out.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))

class SuperChatsFetcherHandler( webapp2.RequestHandler ):

    def post(self):
        logging.info ("Starting to look for superchats")

        channel_creds= Channel.get_barbara_creds()

        if channel_creds is None:
            logging.info("Sponsor Fetcher: No channel")
            return

        logging.info("Checking for new superchats")
        SuperChat.get_superchats( channel_creds, constants.BARBARA_CHANNEL_ID )

        if helpers.is_barbara_live():
            #time.sleep(5)
            task = taskqueue.add( queue_name = "superchats-queue",
                                  url = "/superchats/fetcher"
                                )
        logging.info("No longer looking for new superchats")

app = webapp2.WSGIApplication([ ('/superchats/fetcher', SuperChatsFetcherHandler),
                                ('/superchats/enqueue', EnqueueSuperChatsFetchTaskHandler)
                              ], debug=True)
