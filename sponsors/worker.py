import constants
import httplib2
import json
import logging
import os
import webapp2

from channels.models import Channel
from sponsors.models import Sponsor

from datetime import datetime
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

class EnqueueSponsorsFetchTaskHandler (webapp2.RequestHandler):

    def get(self):

        task = taskqueue.add (
            queue_name = "sponsors-queue",
            url = "/sponsors/fetcher",
            )
        self.response.out.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))

class SponsorsFetcherHandler( webapp2.RequestHandler ):

    def post(self):
        channel = Channel.query(Channel.external_id == constants.BARBARA_CHANNEL_ID).get()

        if channel is None:
            logging.info("Video Fetcher: No channel")
            return

        logging.info("Video Fetcher: Have a channel")
        Sponsor.get_sponsors( channel.credentials )

app = webapp2.WSGIApplication([ ('/sponsors/fetcher', SponsorsFetcherHandler),
                                ('/sponsors/enqueue', EnqueueSponsorsFetchTaskHandler)
                              ], debug=True)
