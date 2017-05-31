import webapp2
import json

from pumpkins.models import Pumpkin

class PumpkinHandler (webapp2.RequestHandler):

    def put(self):
        jsonObject = json.loads(self.request.body)

        requiredFields = ["user_name", "amount", "profile_URL", "x_position",
                          "y_position", "rotation"]

        for requiredField in requiredFields:
            if requiredField in jsonObject:
                continue
            else:
                self.error(400)
                self.response.write('Missing required field "' + requiredField +
                                    '"')
                return

        pumpkin = Pumpkin()
        pumpkin.user_name = jsonObject["user_name"]
        pumpkin.amount = jsonObject["amount"]
        pumpkin.profile_URL = jsonObject ["profile_URL"]
        pumpkin.x_position = jsonObject ["x_position"]
        pumpkin.y_position = jsonObject ["y_position"]
        pumpkin.rotation = jsonObject ["rotation"]
        pumpkin.put()
        return

app = webapp2.WSGIApplication([ ('/pumpkins',PumpkinHandler)
                              ], debug=True)
