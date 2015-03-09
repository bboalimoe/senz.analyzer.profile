import json
from lean_cloud.lean_obj import AVObject

class UserTrainParam(AVObject):

    TRAIN_PARAM_OBJECT_ID = "54f90793e4b0ab818dfae9c2"

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



    def updateTrainParam(self, data):
        # Create the dict of update data
        update_data = {}
        for key, value in data.iteritems():
            update_data[key] = value
        # Update the data in Database
        self.update(self.TRAIN_PARAM_OBJECT_ID, update_data)