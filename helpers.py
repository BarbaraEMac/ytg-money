
import constants

import httplib2
import logging

from apiclient.discovery import build
from google.appengine.api import memcache

def auth_http( credentials ):
    authed_http = build(constants.YOUTUBE_API_SERVICE_NAME,
                  constants.YOUTUBE_API_VERSION,
                  http=credentials.authorize(httplib2.Http()))

    return authed_http

def is_barbara_live():
    return memcache.get( key="BARBARA_IS_LIVE" )

def convert_to_usd( amountMicros, currency ):
    factor = 1

    if currency == "ARS":
        factor = 0.59

    elif currency == "AUD":
        factor = 0.76

    elif currency == "EUR":
        factor = 1.14

    elif currency == "BRL":
        factor = 0.3

    elif currency == "CAD":
        factor = 0.78

    elif currency == "CLP":
        factor = 0.0015

    elif currency == "COP":
        factor = 0.00032

    elif currency == "DKK":
        factor = 0.15

    elif currency == "HKD":
        factor = 0.13

    elif currency == "HUF":
        factor = 0.0037

    elif currency == "INR":
        factor = 0.015

    elif currency == "JPY":
        factor = 0.0088

    elif currency == "MKD":
        factor = 0.019

    elif currency == "MXN":
        factor = 0.055

    elif currency == "NZD":
        factor = 0.73

    elif currency == "NOK":
        factor = 0.12

    elif currency == "PEN":
        factor = 0.31

    elif currency == "PHP":
        factor = 0.02

    elif currency == "PLN":
        factor = 0.27

    elif currency == "RUB":
        factor = 0.017

    elif currency == "XOF":
        factor = 0.0017

    elif currency == "KRW":
        factor = 0.00087

    elif currency == "SEK":
        factor = 0.12

    elif currency == "CHF":
        factor = 1.04

    elif currency == "TWD":
        factor = 0.033

    elif currency == "GBP":
        factor = 1.29

    return float( float(factor) * (amountMicros/1000000) )



