#!/usr/bin/env python

import Constants
import httplib2
import json
import logging
import os
import re
import sys
import webapp2

from channels.models import *

from google.appengine.api import users
from google.appengine.ext.webapp import template
from main.models import *
from oauth2client.contrib.appengine import (CredentialsNDBProperty,
                                            OAuth2DecoratorFromClientSecrets,
                                            StorageByKeyName)

from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

foo = os.path.dirname(__file__) + "/client_secrets.json"
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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

    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url( "/oauth2callback" )

        if user and user.email() != "test@example.com":
            channel = Channel.query(Channel.user_id == user.user_id())

            if channel is None:
                self.redirect("/oauth2callback")
            else:
                self.response.write("USER!! %s %s " % (user.nickname(), users.create_logout_url("/login")))

        else:
            self.redirect( login_url )

class Oauth2CallbackHandler(webapp2.RequestHandler):
    # https://developers.google.com/api-client-library/python/auth/web-app#callinganapi

    def get(self):
        user = users.get_current_user()

        if user is None:
            self.redirect( users.create_login_url('/oauth2callback') )
            return

        flow = flow_from_clientsecrets(foo, scope=YOUTUBE_SCOPE, message=Constants.MISSING_CLIENT_SECRETS_MESSAGE, redirect_uri="http://8080-dot-2163697-dot-devshell.appspot.com/oauth2callback")

        if not self.request.get('code'):
            flow.params['access_type'] = 'offline'   # offline access
            flow.params['prompt'] = 'consent'        # let them consent to it
            auth_uri = flow.step1_get_authorize_url()

            self.redirect( str(auth_uri) )
            return

        else:
            auth_code = self.request.get('code')

            credentials = flow.step2_exchange(auth_code)
            channel = Channel.get_or_create( credentials, user )

            logging.info(channel.external_id)
            self.redirect("/login")
            return

app = webapp2.WSGIApplication([("/", LiveHandler),
                               ("/sponsors", SponsorsHandler),
                               ("/patch", PatchHandler),
                               ("/alerts_api", AlertsApiHandler),
                               ("/login", LoginHandler),
                               ("/oauth2callback", Oauth2CallbackHandler)
                              ],
                              debug=True)
