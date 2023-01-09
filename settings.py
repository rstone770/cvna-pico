import json
import io

class Settings:
    def __init__(self, wlan_ssid = "", wlan_password = "", finhub_apikey = "", poll_interval = 6000):
        self.wlan_ssid = wlan_ssid
        self.wlan_password = wlan_password
        self.finhub_apikey = finhub_apikey
        self.pool_interval = poll_interval

        self.is_valid = True

        if wlan_ssid == "" or wlan_password == "" or finhub_apikey == "":
            self.is_valid = False

def read_settings():
    try:
        file = open("settings.json", "rt")
        data = json.loads(file.read())

        return Settings(data["wlan_ssid"], data["wlan_password"], finhub_apikey=data["finhub_apikey"], poll_interval=data["poll_interval"])
    except (OSError, ValueError) as error:
        print(error)

        return Settings()
