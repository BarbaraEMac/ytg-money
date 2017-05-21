#!/usr/bin/env python

import constants
import httplib2
import json
import logging
import os
import re
import sys
import webapp2

from channels.models import *
from urlparse import urlparse
from google.appengine.api import users
from google.appengine.ext.webapp import template
from main.models import *

from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets

class LiveHandler(webapp2.RequestHandler):
    def get(self):
        channel = Channel.query(Channel.external_id == constants.BARBARA_CHANNEL_ID).get()

        if channel is None:
            self.redirect( "https://gaming.youtube.com/BarbaraEMac?action=subscribe")
            return

        top_live_video = channel.get_top_live_video_id()

        if top_live_video != "":
            self.redirect( "https://gaming.youtube.com/watch?v=%s" % top_live_video)
        else:
            self.redirect( "https://gaming.youtube.com/BarbaraEMac?action=subscribe")

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

        # test@example.com is the default logged in user for devappserver
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

        if os.environ.get('SERVER_SOFTWARE','').startswith('Development'):
            bar = "https://8080-dot-2163697-dot-devshell.appspot.com/oauth2callback"
        else:
            bar = "https://ytg-money.appspot.com/oauth2callback"

        flow = flow_from_clientsecrets(constants.CLIENT_SECRETS,
                                       scope=constants.YOUTUBE_SCOPE,
                                       message=constants.MISSING_CLIENT_SECRETS_MESSAGE,
                                       redirect_uri=bar )

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
