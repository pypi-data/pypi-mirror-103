import requests
import json
import BlynkWrapper.Errors as Errors


class BlynkWrapper():
    def __init__(self, auth_token: str, server_name: str = "blynk-cloud.com", server_port: int = 8080, debug: bool = False):
        self.DEBUG_MODE = debug
        self.config = dict()
        self.config["server_name"] = server_name
        self.config["server_port"] = server_port
        self.config["auth_token"] = auth_token

        self.URL = "http://{}:{}/{}/".format(
            self.config["server_name"], self.config["server_port"], self.config["auth_token"])
        if self.DEBUG_MODE:
            print("Server URL is:\t{}".format(self.URL))

    def get(self, virtual_pin: str) -> int:
        get_URL = "{}get/{}".format(self.URL, virtual_pin)
        response = requests.get(get_URL)
        content = response.content.decode("utf-8")
        if (response.status_code == 400):
            Errors.raiseError(content)
        status = json.loads(content)
        if self.DEBUG_MODE:
            print("GET URL is:\t{}".format(get_URL))
            print("Got Value:\t{}".format(status[0]))
        return status[0]

    def update(self, virtual_pin: str, value: int) -> int:
        parameters = {
            "value": value
        }
        update_URL = "{}update/{}".format(self.URL, virtual_pin)
        response = requests.get(update_URL, parameters)
        if self.DEBUG_MODE:
            print("Update URL is:\t{}".format(response.url))
            print("Update Status is:\t{}".format(response.status_code))
        return response.status_code

    def isConnected(self):
        connected_URL = "{}isHardwareConnected".format(self.URL)
        response = requests.get(connected_URL)
        status = response.content.decode("utf-8")
        if response.status_code == 400:
            Errors.raiseError(status)
        elif status == "true":
            return True
        elif status == "false":
            return False

    def getProjectDetails(self):
        project_Url = "{}project".format(self.URL)
        if self.DEBUG_MODE:
            print("Project URL is: {}".format(project_Url))
        return json.loads(requests.get(project_Url).content)

    def getDevices(self):
        devices = list()
        for device in self.getProjectDetails()["devices"]:
            if self.DEBUG_MODE:
                print("Device Name: {}\tDevice Type: {}\tDevice ID: {}".format(
                    device["name"], device["boardType"], device["id"]))
            devices.append(
                {
                    "deviceName": device.get("name"),
                    "boardType": device.get("boardType"),
                    "id": device.get("id")
                }
            )
        return devices

    def getWidgets(self):
        return self.getProjectDetails()["widgets"]

    def getStyledButtons(self):
        widgets = self.getWidgets()
        styled_buttons = list()
        for widget in widgets:
            if "STYLED_BUTTON" in widget.get("type"):
                styled_buttons.append({
                    "id": widget.get("id"),
                    "label": widget.get("label"),
                    "deviceId": widget.get("deviceId"),
                    "pinType": widget.get("pinType"),
                    "pin": widget.get("pin")
                })
        return styled_buttons


if __name__ == "__main__":

    skill = BlynkWrapper("serverName", 8080, "AuthToken")

    getResponse = skill.get("V3")
    updateResponse = skill.update("V3", 0)

    print(getResponse)
    print(updateResponse)
    print(skill.isConnected())
