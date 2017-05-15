#!/usr/bin/env python

import Constants
import json
import httplib2
import os
import logging
import webapp2

from main.models import *
from apiclient.discovery import build
from oauth2client.contrib.appengine import (CredentialsNDBProperty,
                                            OAuth2DecoratorFromClientSecrets,
                                            StorageByKeyName)

class LiveHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""TST""")

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

app = webapp2.WSGIApplication([("/", LiveHandler),
                               ("/alerts_api", AlertsApiHandler)
                              ],
                              debug=True)