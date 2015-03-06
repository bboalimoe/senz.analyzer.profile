import json
from lean_cloud.lean_obj import AVObject

class UserDeviceInfo(AVObject):

    def __init__(self, device_mac):
        self.deviceMAC = device_mac
        device_info = self._getDeviceInfoByMAC()
        self.userId       = device_info["userIdString"]
        self.serialNumber = device_info["serialNumber"]
        self.sdkVersion   = device_info["sdkVersion"]
        self.resolution   = device_info["resolution"]
        self.dpi          = device_info["dpi"]
        self.abi          = device_info["abi"]
        self.imsi         = device_info["imsi"]
        self.hardware     = device_info["hardware"]
        self.packageList  = self._decodePackageList(device_info["packageList"])



    def _getDeviceInfoByMAC(self):
        # Init the param
        param = {
            "deviceId": self.deviceMAC, # Select items which deviceId is equal to mac.
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




if __name__ == "__main__":

    m = UserDeviceInfo("866707010347352")
