#!/usr/bin/env python

import Constants
import json
import httplib2
import os
import logging
import webapp2

from apiclient.discovery import build
from oauth2client.contrib.appengine import (CredentialsNDBProperty,
                                            OAuth2DecoratorFromClientSecrets,
                                            StorageByKeyName)

class LiveHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""TST""")

app = webapp2.WSGIApplication([("/", LiveHandler)],
                              debug=True)
