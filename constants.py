import os

from google.appengine.api import memcache

# External channel IDs for my 2 channels
BARBARA_CHANNEL_ID = "UCmydrQwDJ12_8vAwRv-aqKw"
BARBBOT_CHANNEL_ID = "UCxhux0GVVyP1iX_nt7cU1bQ"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# FIlepath to teh client secrets json file
CLIENT_SECRETS = os.path.dirname(__file__) + "/client_secrets.json"
# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """ WARNING: Please configure OAuth 2.0"""
