from model.app_table import AppTable
from model.user_device_info import UserDeviceInfo
from model.user_profile import UserProfile
from model.user_train_param import UserTrainParam
from nbcLib.nbc import NBC
import decimal

class Learner(NBC):

    def __init__(self, hypothesis_type):
        # The user's device infomation
        # device_user = UserDeviceInfo(device_mac)
        # self.userId = device_user.userId
        # All kinds of app info in database
        app_set    = AppTable()
        # Logging
        app_set.printAppInfo()
        # All user's info in database
        device_all = UserDeviceInfo()
        # Logging
        device_all.printUserInfo()
        self.hypothesisType = hypothesis_type

        self.case = self._generateCase(
            app_set,        # The universal set of app
            device_all,     # The infomation of all devices in database
            hypothesis_type # THe type of hypothesis that we need learn
        )
        # Logging
        self._printCaseContent()
        # print self.case
        NBC.__init__(self, self.case)



    def _generateCase(self, app_set, device_info_list, hypothesis_type):
        case = {}
        case["item_name"] = app_set.appName
        print device_info_list.userId[0]
        for index in range(0, len(device_info_list.userId)):
            print index
            user = UserProfile(device_info_list.userId[index])
            case[str(index)] = {
                "h":    self.HYPOTHESIS_LIST[hypothesis_type][str(user.userInfo[hypothesis_type])],
                "case": device_info_list.generateTrainCase(app_set.appPackageName)[index]
            }
        return case


    def _printCaseContent(self):
        print "\n\n"
        print "Generated Case Content:"
        print " # The case item include:", self.case["item_name"]
        print " # The case content:"
        for i in range(0, len(self.case.keys())-1):
            print self.case[str(i)]



    # PUBLIC METHOD
    def train(self, m="notInput", p="notInput"):
        # Train
        NBC.train(self, m, p)
        # Store in database
        # print NBC.generateTrainResult(self)
        data = {self.hypothesisType: NBC.generateTrainResult(self)}

        param_hypo = UserTrainParam()
        param_hypo.updateTrainParam(data)


if __name__ == "__main__":

    m = Learner("age")
    m.train()










