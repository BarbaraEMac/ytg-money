#!/usr/bin/env python

import constants
import datetime
import httplib2
import json
import logging
import os
import re
import random
import sys
import webapp2

import helpers

from alerts.models import Alert
from channels.models import *
from main.models import *
from videos.models import *
from viewers.models import *

from apiclient.errors import HttpError
from google.appengine.api import users
from google.appengine.ext.webapp import template
from oauth2client.client import flow_from_clientsecrets

class PatchHandler(webapp2.RequestHandler):

    def get(self):
        self.response.out.write( template.render("main/templates/webGL/index.html",{}) )

class AlertsApiHandler(webapp2.RequestHandler):

    def get(self):
       # if (datetime.now().second % 10 != 0):
       #     return

        alert_response = []

        dollarAmounts = [1, 2, 5, 10, 20, 50, 100]
        i = random.randrange(len(dollarAmounts) - 1)
        amount = random.choice(dollarAmounts)

        alert_response.append( {
                'type': "SUB",
                'id': 'uuid' + str(random.randint(0,10000000)), #str(i),
                'channel_id': 'channel:' + str(i),
                'name': 'Curious George' + str(amount),
                'image' : 'https://yt3.ggpht.com/-KvBjE1iQ-Yk/AAAAAAAAAAI/AAAAAAAAAAA/8y92vRZBW2s/s88-c-k-no-mo-rj-c0xffffff/photo.jpg',
                'text': 'msg' + str (amount),
                'amount' : amount,
                'sponsor' : i % 2
                })

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( json.dumps({'alerts': alert_response}) )

class LiveHandler(webapp2.RequestHandler):
    def get(self):
        # If in the dev server, don't redirect
        if os.environ.get('SERVER_SOFTWARE','').startswith('Development'):
            self.response.out.write("Hello and welcome to our dev server")
            return
        channel_creds = Channel.get_barbara_creds()

        if channel_creds is None:
            logging.info("No channel found. Redirecting to channel page")
            self.redirect( "https://www.youtube.com/channel/UCmydrQwDJ12_8vAwRv-aqKw?sub_confirmation=1")
            return

        logging.info("Fetching top live videos")
        if helpers.is_barbara_live():

            top_live_video = Video.get_top_live_video_id( channel_creds )

            if top_live_video != "":
                self.redirect( "https://www.youtube.com/watch?v=%s" % top_live_video)

        self.redirect( "https://www.youtube.com/channel/UCmydrQwDJ12_8vAwRv-aqKw?sub_confirmation=1")

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

class RaidHandler (webapp2.RequestHandler):

    def get(self):
        self.response.out.write( template.render("main/templates/raid.html",{}) )

class SubsPageHandler (webapp2.RequestHandler):

    def get(self):
        self.response.out.write( template.render("main/templates/subs.html",{}) )

class SubsAlertsHandler(webapp2.RequestHandler):

    def get(self):
        alert_response = []

        subs = Viewer.query( Viewer.is_sub == True ).order( -Viewer.created_date ).fetch( 10 )

        for sub in subs:
            logging.info("Getting most recent sub " + str(sub.created_date) + " " + sub.channel_id + " " + sub.name + " " + sub.image);
            alert_response.append( {
                    'id': sub.channel_id,
                    'name': sub.name,
                    'image' : sub.image
                   })

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( json.dumps({'alerts': alert_response}) )

class PumpkinImageHandler (webapp2.RequestHandler):

    def get(self):
        self.response.out.write( template.render("main/templates/pumpkinImage.html",{}) )

class MoneyPageHandler (webapp2.RequestHandler):

    def get(self):
        self.response.out.write( template.render("main/templates/money.html",{}) )

class MoneyAlertsHandler(webapp2.RequestHandler):

    def get(self):
        alert_response = []

        dollarAmounts = [1, 2, 5, 10, 20, 50, 100]
        i = random.randrange(len(dollarAmounts) - 1)
        amount = random.choice(dollarAmounts)

        alert_response.append( {
                'type': "SUPER",
                'id': 'uuid' + str(random.randint(0,10000000)), #str(i),
                'channel_id': 'channel:' + str(i),
                'name': 'Curious George' + str(amount),
                'image' : 'https://yt3.ggpht.com/-KvBjE1iQ-Yk/AAAAAAAAAAI/AAAAAAAAAAA/8y92vRZBW2s/s88-c-k-no-mo-rj-c0xffffff/photo.jpg',
                'text': 'msg' + str (amount),
                'amount' : amount,
                'sponsor' : i % 2
                })

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( json.dumps({'alerts': alert_response}) )

class TipHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect("https://streamlabs.com/BarbaraEMac")

class SubHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect( "https://www.youtube.com/channel/UCmydrQwDJ12_8vAwRv-aqKw?sub_confirmation=1")

class SponsorHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect( "https://www.youtube.com/user/BarbaraEMac/sponsor")

class MerchHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect( "https://www.teespring.com/stores/BarbaraEMac")

class TwitterHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect( "https://www.twitter.com/BarbaraEMac")

class InstaHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect( "https://www.instagram.com/BarbaraEMac")

class DiscordHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect( "https://discord.gg/3XyNWRc")


class TwitchHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect( "https://www.twitch.tv/BarbaraEMac")

class MixerHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect( "https://www.mixer.com/BarbaraEMac")

class FBHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect( "https://www.facebook.com/gaming/BarbaraEMac")

app = webapp2.WSGIApplication([("/", LiveHandler),
                               ("/patch", PatchHandler),
                               ("/alerts_api", AlertsApiHandler),
                               ("/login", LoginHandler),
                               ("/oauth2callback", Oauth2CallbackHandler),
                               ("/raid", RaidHandler),
                               ("/pumpkinImage", PumpkinImageHandler),
                               ("/subs", SubsPageHandler),
                               ("/subsAlerts", SubsAlertsHandler),
                               ("/money", MoneyPageHandler),
                               ("/moneyAlerts", MoneyAlertsHandler),
                               (r'/(?i)tip.*', TipHandler),
                               (r'/(?i)sub.*', SubHandler),
                               (r'/(?i)subscribe.*', SubHandler),
                               (r'/(?i)sponsor.*', SponsorHandler),
                               (r'/(?i)merch.*', MerchHandler),
                               (r'/(?i)twitter.*', TwitterHandler),
                               (r'/(?i)insta.*', InstaHandler),
                               (r'/(?i)discord.*', DiscordHandler),
                               (r'/(?i)twitch.*', TwitchHandler),
                               (r'/(?i)mixer.*', MixerHandler),
                               (r'/(?i)fb.*', FBHandler)
                              ],
                              debug=True)
