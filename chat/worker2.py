import constants
import helpers
import logging
import time
import webapp2

from channels.models import Channel
from videos.models   import Video

from google.appengine.api import taskqueue

class EnqueueChatFetchTaskHandler (webapp2.RequestHandler):

    def get(self):

        task = taskqueue.add( queue_name = "chat-queue",
                              url = "/chat/fetcher"
                            )
        self.response.out.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))

class ChatFetcherHandler( webapp2.RequestHandler ):

    def post(self):
        logging.info ("Starting to look for chat")

        channel_creds= Channel.get_barbara_creds()

        if channel_creds is None:
            logging.info("Chat Fetcher: No channel")
            return

        logging.info("Checking for new chat")
        Sponsor.get_chat( channel_creds, constants.BARBARA_CHANNEL_ID )

        if helpers.is_barbara_live():
            #time.sleep(5)
            task = taskqueue.add( queue_name = "chat-queue",
                                  url = "/chat/fetcher"
                                )
        logging.info("No longer looking for new Chat")

app = webapp2.WSGIApplication([ ('/chat/fetcher', ChatFetcherHandler),
                                ('/chat/enqueue', EnqueueChatFetchTaskHandler)
                              ], debug=True)
