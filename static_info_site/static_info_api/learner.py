from model.app_table import AppTable
from model.user_device_info import UserDeviceInfo
from model.user_profile import UserProfile
from model.user_train_param import UserTrainParam
from nbcLib.nbc import NBC

class Learner(NBC):

    HYPOTHESIS_LIST = {
        "age": {"0": "10-18", "19": "19-26", "27": "27-35"}
    }

    def __init__(self, device_mac, hypothesis_type):
        app_set     = AppTable()
        device_all  = UserDeviceInfo()
        device_user = UserDeviceInfo(device_mac)

        self.userId    = device_user.userId
        self.caseHypothesisType = hypothesis_type
        self.caseValueList  = device_all.generateTrainCase(app_set.appPackageName)
        self.caseUserIdList = device_all.userId

        self.case = self._generateCase(
            app_set,        # The universal set of app
            device_all,     # The infomation of all devices in database
            hypothesis_type # THe type of hypothesis that we need learn
        )
        print self.case
        nbc = NBC(self.case)




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


if __name__ == "__main__":

    m = Learner("866707010347352", "age")









