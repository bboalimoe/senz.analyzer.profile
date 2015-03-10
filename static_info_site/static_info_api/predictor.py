from model.app_table import AppTable
from model.user_device_info import UserDeviceInfo
from model.user_profile import UserProfile
from model.user_train_param import UserTrainParam
from nbcLib.nbc import NBC

class Predictor(NBC):

    HYPOTHESIS_RELIABILITY_ATTRIBUTE_NAME = {
        "age": "ageReliability"
    }

    def __init__(self, device_mac):
        # The user's device infomation
        device_user = UserDeviceInfo(device_mac)
        # All kinds of app info in database
        app_set     = AppTable()

        self.userId      = device_user.userId
        self.predictCase = device_user.generateTrainCase(app_set.appPackageName)
        NBC.__init__(self)



    def _generateUserFeature(self, hypothesis_type, hypothesis_reliability):
        max_h     = ""
        max_p     = 0

        for h in hypothesis_reliability:
            if hypothesis_reliability[h] > max_p:
                max_p = hypothesis_reliability[h]
                max_h = h
        for feature in self.HYPOTHESIS_LIST[hypothesis_type]:
            # What is the different between '==' and 'is'???
            # Here 'is' is wrong, we should put '==' here!!!
            if str(self.HYPOTHESIS_LIST[hypothesis_type][feature]) == str(max_h):
                return feature



    # PUBLIC METHOD
    def predict(self, hypothesis_type):
        user_train_param = UserTrainParam()
        param            = user_train_param.getParamInfoByHypothesis(hypothesis_type)
        hypothesis_list  = param["hypothesis"]
        # rebuild the NBC's model with param from database
        NBC.rebuildNBCModel(
            self,
            hypothesis_list,
            param["priorP"],
            param["likelihoodP"]
        )
        # predict the user's case
        reliability = NBC.predictCase(self, self.predictCase)
        update_data            = {
            hypothesis_type: int(self._generateUserFeature(hypothesis_type, reliability)),
            self.HYPOTHESIS_RELIABILITY_ATTRIBUTE_NAME[hypothesis_type]: reliability
        }
        print update_data
        user_profile = UserProfile(self.userId)
        user_profile.updateUserInfo(update_data)

if __name__ == "__main__":

    m = Predictor("866707010347352")
    m.predict("age")