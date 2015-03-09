from model.app_table import AppTable
from model.user_device_info import UserDeviceInfo
from model.user_profile import UserProfile
from model.user_train_param import UserTrainParam
from nbcLib.nbc import NBC

class Predictor(NBC):

    HYPOTHESIS_LIST = {
        "age": {"0": "10-18", "19": "19-26", "27": "27-35"}
    }

    def __init__(self, device_mac, hypothesis_type):
        # The user's device infomation
        device_user = UserDeviceInfo(device_mac)
        self.userId = device_user.userId
        # All kinds of app info in database
        app_set     = AppTable()
        # All user's info in database
        device_all  = UserDeviceInfo()
        # The user's trainning param
        param       = UserTrainParam()

        self.case = self._generateCase(
            app_set,        # The universal set of app
            device_all,     # The infomation of all devices in database
            hypothesis_type # THe type of hypothesis that we need learn
        )
        # print self.case
        NBC.__init__(self, self.case)