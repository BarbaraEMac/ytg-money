#!/usr/bin/env python

import Constants
import json
import httplib2
import os
import logging
import webapp2

from google.appengine.ext.webapp import template
from main.models import *
from apiclient.discovery import build
from oauth2client.contrib.appengine import (CredentialsNDBProperty,
                                            OAuth2DecoratorFromClientSecrets,
                                            StorageByKeyName)

BASE_URL = "https://www.googleapis.com/youtube/v3/"
AUTH_ARGS = {'access_type':'offline'}
OAUTH_DECORATOR = OAuth2DecoratorFromClientSecrets(
            os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
                'https://www.googleapis.com/auth/youtube',
                    **AUTH_ARGS)

class LiveHandler(webapp2.RequestHandler):
    def get(self):

        #storage = StorageByKeyName(CredentialsModel, channel_id, 'credentials')
        #storage.put(OAUTH_DECORATOR.credentials)

        #video_id = self.request.get('videoId')
        #videos = youtube.videos().list(id=video_id, part="liveStreamingDetails").execute()

        #logging.info(videos['items'])
        #if len(videos['items']) == 0:
        #    self.response.write("""Channel is not live""")
        #    return

        #video = videos['items'][0]
        #live_chat_id = video['liveStreamingDetails']['activeLiveChatId']

        self.response.out.write("""Not live""")

class SponsorsHandler(webapp2.RequestHandler):
    def get(self):

        storage = ndb.Key(CredentialsModel, Constants.BARBARA)
        credential = storage.get()
        if credential is None:
            raise Exception("bad creds")

        http = httplib2.Http()
        http = credential.credentials.authorize(http)
        resp, data = http.request("%ssponsors?part=snippet&maxResults=5&filter=all" % BASE_URL)
        data = json.loads(data)
        if 'error' in data:
            raise Exception("Error fetching sponsors: %s" % json.dumps(data['error']))

        self.response.out.write( json.dumps({'alerts': data}) )

class PatchHandler(webapp2.RequestHandler):

    def get(self):
        self.response.out.write( template.render("main/templates/webGL/index.html",{}) )

class AlertsApiHandler(webapp2.RequestHandler):

    def get(self):

        alert_response = []

        for i in range(1,10):
            alert_response.append( {
                'id': 'uuid' + str(i),
                'name': 'Curious George' + str(i),
                'image' : 'https://upload.wikimedia.org/wikipedia/en/d/d8/Curious_George.png',
                'text': 'msg' + str (i),
                'amount' : i,
                'sponsor' : i % 2
                })

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( json.dumps({'alerts': alert_response}) )



class LoginHandler(webapp2.RequestHandler):
    """We only want to use this website with 2 accounts"""

    @OAUTH_DECORATOR.oauth_aware
    def get(self):
        if not self.request.get("secret"):
            self.response.write("you forgot the password")
            return

        # If someone is logged in:
        if OAUTH_DECORATOR.has_credentials():

            http = OAUTH_DECORATOR.http()
            youtube = build('youtube', 'v3', http=http)
            channel = youtube.channels().list(mine=True, part='id').execute()
            channel_id = channel['items'][0]['id']

            storage = StorageByKeyName(CredentialsModel, channel_id, 'credentials')
            storage.get()

            # Refresh Barbara's channel oauth tokens
            if self.request.get('secret') == "channel": # and channel_id != Constants.BARBARA:
                logging.info("Trying to store the channel")
                storage.locked_get().revoke(httplib2.Http())
                url = OAUTH_DECORATOR.authorize_url()
                self.redirect( url )

            # Refresh BarbBot's oauth tokens
            elif self.request.get('secret') == "bot" and channel_id != Constants.BARBBOT:
                storage.locked_get().revoke(httplib2.Http())
                url = OAUTH_DECORATOR.authorize_url()
                self.redirect( url )

            self.response.write("""Using """+channel_id)

        else:
            logging.info("NO ONE")
            url = OAUTH_DECORATOR.authorize_url()
            self.redirect( url )

app = webapp2.WSGIApplication([("/", LiveHandler),
                               ("/sponsors", SponsorsHandler),
                               ("/patch", PatchHandler),
                               ("/alerts_api", AlertsApiHandler),
                               ("/login", LoginHandler),
                               (OAUTH_DECORATOR.callback_path, OAUTH_DECORATOR.callback_handler())
                              ],
                              debug=True)
