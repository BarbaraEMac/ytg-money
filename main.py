#!/usr/bin/env python

import os
import logging

import webapp2

from google.appengine.api import memcache, taskqueue
from google.appengine.ext import ndb

from apiclient.discovery import build
from oauth2client.contrib.appengine import (CredentialsNDBProperty,
                                            OAuth2DecoratorFromClientSecrets,
                                            StorageByKeyName)

AUTH_ARGS = {'access_type':'offline'}

OAUTH_DECORATOR = OAuth2DecoratorFromClientSecrets(
    os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
    'https://www.googleapis.com/auth/youtube',
    **AUTH_ARGS)

class CredentialsModel(ndb.Model):
    """Test"""
    credentials = CredentialsNDBProperty()

class MainHandler(webapp2.RequestHandler):
    """Entry point for our web app."""
    @OAUTH_DECORATOR.oauth_required
    def get(self):
        """Handler for GET requests to the app."""
        logging.info("Handling the get")
	http = OAUTH_DECORATOR.http()
        if not self.request.get('videoId'):
            self.response.write("""Please supply the video ID of a YouTube live stream as a query
                                parameter, i.e. ?videoId=xxx.""")
            return

        youtube = build('youtube', 'v3', http=http)
        channel = youtube.channels().list(mine=True, part='id').execute()
        channel_id = channel['items'][0]['id']

        storage = StorageByKeyName(CredentialsModel, channel_id, 'credentials')
        storage.put(OAUTH_DECORATOR.credentials)

        video_id = self.request.get('videoId')
        videos = youtube.videos().list(id=video_id, part="liveStreamingDetails").execute()
        
	logging.info(videos['items'])
	if len(videos['items']) == 0:
            self.response.write("""Channel is not live""")
            return
	
	video = videos['items'][0]
        live_chat_id = video['liveStreamingDetails']['activeLiveChatId']

        # See if the bot's already in the channel.
        in_chat = memcache.get("{}:in_chat".format(live_chat_id))
        if in_chat:
            self.response.write("""The bot's already in that chat! Try saying .hi to
             it, or asking it to .leave! If the bot isn't in chat, wait 4 minutes
            then try adding it again""")
        else:
            taskqueue.add(url='/spawnbot', target='worker', params=
                          {'channel_id':channel_id,
                           'live_chat_id':live_chat_id})

    	taskqueue.add(url='/sponsorbot', target='worker', params=
		  {'channel_id':channel_id,
		   'live_chat_id':live_chat_id})
    	
	self.response.write("Created the bot task for live chat "+live_chat_id
                                +" on channel "+channel_id+
                                "! The bot should join the channel soon and say hello :)")

app = webapp2.WSGIApplication([("/", MainHandler),
                               (OAUTH_DECORATOR.callback_path, OAUTH_DECORATOR.callback_handler())],
                              debug=True)
