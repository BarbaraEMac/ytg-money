import uuid

from viewers.models import Viewer

from datetime import datetime
from google.appengine.ext import ndb

class Alert(ndb.Model):
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    id = ndb.StringProperty(indexed=False)

    has_been_run = ndb.BooleanProperty(default=False, indexed=True)

    viewer = ndb.StructuredProperty(Viewer)

    text = ndb.StringProperty(indexed=False)

    amount = ndb.FloatProperty(indexed=False)

    type = ndb.StringProperty(indexed=True)

    @staticmethod
    def create_sponsor_alert( viewer ):
        alert = Alert( id     = uuid.uuid1(),
                       viewer = viewer,
                       text   = "",
                       amount = "3.99",
                       type   = "SPONSOR" )
        alert.put()


    @staticmethod
    def create_super_chat_alert( viewer, text, amount ):
        alert = Alert( id     = uuid.uuid1(),
                       viewer = viewer,
                       text   = text,
                       amount = amount,
                       type   = "SUPER_CHAT" )
        alert.put()

    @staticmethod
    def create_sub_alert( viewer ):
        alert = Alert( id     = uuid.uuid1(),
                       viewer = viewer,
                       text   = "",
                       amount = "",
                       type   = "SUB" )
        alert.put()

    @staticmethod
    def get_alerts_to_run():
        return Alert.query( Alert.has_been_run == False ).fetch()

    @staticmethod
    def mark_as_run( alerts ):
        for alert in alerts:
            alert.has_been_run = True
            alert.put()
