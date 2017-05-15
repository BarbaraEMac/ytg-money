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

class LiveHandler(webapp2.RequestHandler):
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
        self.response.out.write( template.render("main/templates/patch.html",{}) )

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
                               ("/patch", PatchHandler),
                               ("/alerts_api", AlertsApiHandler)
                              ],
                              debug=True)
