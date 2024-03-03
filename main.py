from LEDInterfacer import LEDInterfacer
from wifi_tools import wifi
from displayInterfacer import LCD
from giegerInterfacer import GeigerCounter
from machine import Pin
import json
import time
import config
import logging

def wifi_setup(ssid, password, country):
    wifi_connection = wifi(ssid, password, country)
    wifi_connection.connect()
    return wifi_connection

logging.basicConfig(level=logging.DEBUG)
led = LEDInterfacer()
display = LCD(config.display)
display.text("starting up")
geigercounter = GeigerCounter(26, led)

while True:
    time.sleep(1)
    cpm, usvh = geigercounter.cpm
    display.display_data({"cpm": cpm, "usv/h": usvh})



