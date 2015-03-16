import json
from lean_cloud.lean_obj import AVObject

class AppTable(AVObject):

    def __init__(self, package_name=None):
        if package_name is None:
            self.appPackageName = []
            self.appCatagory    = []
            self.appName        = []
            # self.appIcon        = []
            app_info = self._getAppInfo()
            self.appCount       = len(app_info)
            for i in app_info:
                self.appPackageName.append(str(i["appPackageName"]))
                self.appCatagory.append(i["appCatagory"]) # appCatagory is ascii, it cannot be encode character
                self.appName.append(i["appName"]) # appName is ascii, it cannot be encode character
                # self.appIcon.append(str(i["appIcon"]))
        else:
            app_info = self._getAppInfo(package_name)
            self.appPackageName = package_name
            self.appCatagory    = app_info["appCatagory"] # appCatagory is ascii, it cannot be encode character
            self.appName        = app_info["appName"] # appName is ascii, it cannot be encode character
            # self.appIcon        = app_info["appIcon"]



    def _getAppInfo(self, package_name=None):
        # Get all data from database
        if package_name is None:
            # Get device info
            response = self.get()
            # return json format result
            # print json.loads(response.content)
            return json.loads(response.content)["results"]
        # Get one tuple from database by device mac
        else:
            # Init the param
            param = {
                "appPackageName": package_name, # Select items which deviceId is equal to mac.
            }
            # Get device info
            response = self.get(
                where=param,       # deviceId is equal to mac in Database.
                limit=1,           # Select 1 item of result.
            )
            # return json format result
            # print json.loads(response.content)
            return json.loads(response.content)["results"][0]



    def printAppInfo(self):
        print "\n\n"
        print "Collected APP infomation: (", self.appCount, ")"
        for i in range(0, self.appCount):
            print " *", self.appName[i], ": \tTYPE", self.appCatagory[i], "\tPACKAGE", self.appPackageName[i]



if __name__ == "__main__":

    m = AppTable("com.fingersoft.cartooncamera")
    print m.appPackageName
    print m.appCatagory
    print m.appName