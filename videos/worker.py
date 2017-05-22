import constants
import httplib2
import json
import logging
import os
import webapp2

from channels.models import Channel

from datetime import datetime
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

class EnqueueVideoFetchTaskHandler (webapp2.RequestHandler):

    def get(self):

        task = taskqueue.add (
            queue_name = "videos-queue",
            url = "/videos/live_fetcher",
            )
        self.response.out.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))

class LiveVideosFetcherHandler( webapp2.RequestHandler ):

    def post(self):
        channel = Channel.query(Channel.external_id == constants.BARBARA_CHANNEL_ID).get()

        if channel is None:
            logging.info("Video Fetcher: No channel")
            return

        logging.info("Video Fetcher: Have a channel")
        channel.get_and_save_live_videos()

app = webapp2.WSGIApplication([ ('/videos/live_fetcher', LiveVideosFetcherHandler),
                                ('/videos/enqueue', EnqueueVideoFetchTaskHandler)
                              ], debug=True)