#!/usr/bin/env python

import Constants
import json
import httplib2
import os
import jinja2
import logging
import webapp2

from main.models import *
from apiclient.discovery import build
from oauth2client.contrib.appengine import (CredentialsNDBProperty,
                                            OAuth2DecoratorFromClientSecrets,
                                            StorageByKeyName)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class PlayerHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('webGL_build/index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([("/pumpkin_patch/player", PlayerHandler)
                              ],
                              debug=True)
