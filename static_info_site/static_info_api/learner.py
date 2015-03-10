from model.app_table import AppTable
from model.user_device_info import UserDeviceInfo
from model.user_profile import UserProfile
from model.user_train_param import UserTrainParam
from nbcLib.nbc import NBC
import decimal

class Learner(NBC):

    HYPOTHESIS_LIST = {
        "age": {"0": "10-18", "19": "19-26", "27": "27-35"}
    }

    def __init__(self, hypothesis_type):
        # The user's device infomation
        # device_user = UserDeviceInfo(device_mac)
        # self.userId = device_user.userId
        # All kinds of app info in database
        app_set    = AppTable()
        # All user's info in database
        device_all = UserDeviceInfo()
        self.hypothesisType = hypothesis_type

        self.case = self._generateCase(
            app_set,        # The universal set of app
            device_all,     # The infomation of all devices in database
            hypothesis_type # THe type of hypothesis that we need learn
        )
        # print self.case
        NBC.__init__(self, self.case)



    def _generateCase(self, app_set, device_info_list, hypothesis_type):
        case = {}
        case["item_name"] = app_set.appName
        for index in range(0, len(device_info_list.userId)-1):
            user = UserProfile(device_info_list.userId[index])
            case[str(index)] = {
                "h":    self.HYPOTHESIS_LIST[hypothesis_type][str(user.userInfo[hypothesis_type])],
                "case": device_info_list.generateTrainCase(app_set.appPackageName)[index]
            }
        return case



    # PUBLIC METHOD
    def train(self, m="notInput", p="notInput"):
        # Train
        NBC.train(self, m, p)
        # Store in database
        # print NBC.generateTrainResult(self)
        print self.hypothesis
        for key, value in NBC.generateTrainResult(self).iteritems():
            print key, value
        data = {self.hypothesisType: NBC.generateTrainResult(self)}

        param_hypo = UserTrainParam()
        param_hypo.updateTrainParam(data)


if __name__ == "__main__":

    m = Learner("age")
    m.train()










