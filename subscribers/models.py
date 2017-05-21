import constants
import httplib2
import json
import logging
import os

from channels import Channel

from google.appengine.api import users
from google.appengine.ext import ndb
from oauth2client.contrib.appengine import CredentialsNDBProperty
from apiclient.discovery import build

# https://developers.google.com/youtube/v3/live/docs/sponsors

class Subscribers(ndb.Model):
    channel = ndb.StructuredProperty(channels.Channel)

    num = ndb.IntegerProperty()

    goal ndb.IntegerProperty()
