from videos.models import Video

from google.appengine.ext import ndb

class Viewer(ndb.Model):
    # Added this object was created
    created_date = ndb.DateTimeProperty(auto_now_add=True, indexed=True)

    # YouTube channel id
    channel_id = ndb.StringProperty(default="", indexed=True)

    # YouTube channel url
    channel_url = ndb.StringProperty(default="", indexed=True)

    # Channel's display name
    name = ndb.StringProperty(default="", indexed=False)

    # Profile image URL
    image = ndb.StringProperty(indexed=False)

    num_streams = ndb.IntegerProperty()

    first_stream = ndb.StructuredProperty(Video)
    most_recent_stream = ndb.StructuredProperty(Video)

    all_streams = ndb.StructuredProperty(Video, repeated=True)

    super_chat_total = ndb.FloatProperty(default=0)

    is_sponsor = ndb.BooleanProperty(default=False)

    is_sub = ndb.BooleanProperty(default=False, indexed=True)

    first_chat = ndb.TextProperty()
