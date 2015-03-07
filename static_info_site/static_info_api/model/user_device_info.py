import json
from lean_cloud.lean_obj import AVObject

class UserDeviceInfo(AVObject):

    def __init__(self, device_mac=None):
        self.deviceMAC = device_mac
        if self.deviceMAC is None:
            device_info = self._getDeviceInfo()
            self.packageList = []
            self.hardware    = []
            for i in device_info:
                self.packageList.append(self._decodePackageList(i["packageList"]))
                self.hardware.append(str(i["hardware"]))
                self.userId.append(str(i["userIdString"]))
        else:
            device_info = self._getDeviceInfo(self.deviceMAC)
            self.userId       = str(device_info["userIdString"])
            self.serialNumber = str(device_info["serialNumber"])
            self.sdkVersion   = device_info["sdkVersion"]
            self.resolution   = str(device_info["resolution"])
            self.dpi          = device_info["dpi"]
            self.abi          = str(device_info["abi"])
            self.imsi         = str(device_info["imsi"])
            self.hardware     = str(device_info["hardware"])
            self.packageList  = self._decodePackageList(device_info["packageList"])



    def _getDeviceInfo(self, device_mac=None):
        # Get all data from database
        if device_mac is None:
            # Get device info
            response = self.get()
            # return json format result
            # print json.loads(response.content)
            return json.loads(response.content)["results"]
        # Get one tuple from database by device mac
        else:
            # Init the param
            param = {
                "deviceId": device_mac, # Select items which deviceId is equal to mac.
            }
            # Get device info
            response = self.get(
                where=param,       # deviceId is equal to mac in Database.
                limit=1,           # Select 1 item of result.
            )
            # return json format result
            # print json.loads(response.content)
            return json.loads(response.content)["results"][0]



    def _decodePackageList(self, package_list):
        return package_list.split(', ')



    # PUBLIC METHOD
    def generateTrainCase(self, universal_set):
        case = []
        # If there is only one user device
        if type(self.hardware) is str:
            for index in range(0, len(universal_set)-1):
                if self.packageList[index] is universal_set[index]:
                    case.append(1)
                else:
                    case.append(0)
        # If there are not only one user devices
        elif type(self.hardware) is list:
            for package_list in self.packageList:
                case_item = []
                for index in range(0, len(universal_set)-1):
                    if package_list[index] is universal_set[index]:
                        case_item.append(1)
                    else:
                        case_item.append(0)
                case.append(case_item)
        return case





if __name__ == "__main__":

    m = UserDeviceInfo()