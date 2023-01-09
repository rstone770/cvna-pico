from network import WLAN, STA_IF
from time import sleep_ms

def wifi_connect(ssid: str, password: str):
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while wlan.isconnected() == False:
        sleep_ms(500)
    
    return wlan.ifconfig()[0]
