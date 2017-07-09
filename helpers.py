
import constants

import httplib2
import logging

from apiclient.discovery import build

def auth_http( credentials ):
    authed_http = build(constants.YOUTUBE_API_SERVICE_NAME,
                  constants.YOUTUBE_API_VERSION,
                  http=credentials.authorize(httplib2.Http()))

    return authed_http

def is_barbara_live():
    return memcache.get( key="BARBARA_IS_LIVE" )
