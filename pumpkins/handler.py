import webapp2
import json
import logging

from google.appengine.ext import ndb
from pumpkins.models import Pumpkin

class PumpkinHandler (webapp2.RequestHandler):

    def get(self):
        q = Pumpkin.query()
        results = q.fetch()
        serializableResults = [result.to_dict() for result in results]

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'pumpkins': serializableResults}))

    def post(self):
        requiredFields = ["id","user_name", "amount", "profile_URL", 
                          "x_position", "y_position", "rotation"]

        for requiredField in requiredFields:
            values = self.request.get_all(requiredField)
            if len(values) <= 0:
                self.error(400)
                errStr = 'Request requires field "' + requiredField + '"'
                self.response.write(errStr)                                    
                logging.info(errStr)
                return

        pumpkinID = self.request.get("id")
        pumpkinKey = ndb.Key('Pumpkin', pumpkinID)
        pumpkin = Pumpkin(key = pumpkinKey)
        pumpkin.id = pumpkinID
        pumpkin.user_name = self.request.get("user_name")
        pumpkin.amount = int(self.request.get("amount"))
        pumpkin.profile_URL = self.request.get("profile_URL")
        pumpkin.x_position = float(self.request.get("x_position"))
        pumpkin.y_position = float(self.request.get("y_position"))
        pumpkin.rotation = float(self.request.get("rotation"))
        pumpkin.put()
        return

app = webapp2.WSGIApplication([ ('/pumpkins',PumpkinHandler)
                              ], debug=True)
