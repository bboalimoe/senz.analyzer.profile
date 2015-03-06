import json
from lean_cloud.lean_obj import AVObject

class UserProfile(AVObject):
    def __init__(self, user_id):
        self.userId = user_id
        user_info = self._getUserInfoByUserId()
        self.objectId     = user_info["objectId"]
        self.age          = user_info["age"]
        self.hasParent    = user_info["hasParent"]
        self.curious      = user_info["curious"]
        self.exercise     = user_info["exercise"]
        self.hasPet       = user_info["hasPet"]
        self.isPregnant   = user_info["isPregnant"]
        self.studyAbroad  = user_info["studyAbroad"]
        self.socialManiac = user_info["socialManiac"]
        self.education    = user_info["education"]
        self.gender       = user_info["gender"]
        self.shopManiac   = user_info["shopManiac"]
        self.isSampleData = user_info["isSampleData"]



    def _getUserInfoByUserId(self):
        # Init the param
        param = {
            "userIdString": self.userId, # Select items which deviceId is equal to mac.
        }
        # Get device info
        response = self.get(
            where=param,       # deviceId is equal to mac in Database.
            limit=1,           # Select 1 item of result.
        )
        # return json format result
        return json.loads(response.content)["results"][0]



    # PUBLIC METHOD
    def updateUserInfo(self, **data):
        update_data = {"objectId": self.objectId}
        for key, value in data.iteritems():
            update_data[key] = value
        print update_data
        # Update the data in Database
        self.update_all(update_data)

if __name__ == "__main__":

    m = UserProfile("54d82fefe4b0d414801050ee")
