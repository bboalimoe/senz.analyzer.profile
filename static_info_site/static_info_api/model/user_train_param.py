import json
from lean_cloud.lean_obj import AVObject

class UserTrainParam(AVObject):

    def __init__(self):
        pass

    def getParamInfoByHypothesis(self, hypothesis):
        # Get device info
        response = self.get(
            order="-timestamp", # Timestamp in Ascended order.
            limit=1,            # Select 1 item of result.
            keys=hypothesis
        )
        # return json format result
        return json.loads(response.content)["results"][0][hypothesis]



    def addNewTrainParam(self, hypothesis, value):
        # Init the param
        param = {
            "timestamp": self.Date(), # The current time (formate: iso 8601)
            hypothesis:  value
        }
        self.save(param)