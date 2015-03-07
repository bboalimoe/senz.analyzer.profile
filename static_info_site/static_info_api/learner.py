from model.app_table import AppTable
from model.user_device_info import UserDeviceInfo
from model.user_profile import UserProfile
from model.user_train_param import UserTrainParam
from nbcLib.nbc import NBC

class Learner(NBC):

    def __init__(self, device_mac, hypothesis_type):
        app_set     = AppTable()
        device_all  = UserDeviceInfo()
        device_user = UserDeviceInfo(device_mac)

        self.userId    = device_user.userId
        self.caseHypothesisType = hypothesis_type
        self.caseValueList  = device_all.generateTrainCase(app_set.appPackageName)
        self.caseUserIdList = device_all.userId



    

