from machine import Pin, ADC ,Timer
import usocket as socket
import network
import math

from time import sleep
from constants import *

from hcsr04 import HCSR04

import esp
esp.osdebug(None)

import gc
gc.collect()

import json

#------------------- Sensor----------------------
jsn_sensor = HCSR04(trigger_pin=JSN_TRIGGER_PIN, echo_pin=JSN_ECHO_PIN, echo_timeout_us=JSN_ECHO_TIMEOUT)

#------------------- relays----------------------
relay1 = Pin(RELAY_1_PIN,Pin.OUT)
relay2 = Pin(RELAY_2_PIN,Pin.OUT)
relay3 = Pin(RELAY_3_PIN,Pin.OUT)
relay4 = Pin(RELAY_4_PIN,Pin.OUT)

#------------- relays default value -----------------
relay1.value(not False)
relay2.value(not False)
relay3.value(not False)
relay4.value(not False)


# --------------------------------------------------


with open("data.json", "r") as jsonFile:
    data = json.load(jsonFile)
    
    
#     print("_________________________________")
#     print("data : ", data)
#     print("_________________________________")

    
    
    PROJECT_NAME = data['PROJECT_NAME']
    AUTO = data['AUTO']
    
    WATER_TANK = data['WATER_TANK']
    W_TANK_HEIGHT = WATER_TANK["WATER_TANK_HEIGHT"]
    W_TANK_RADIUS = WATER_TANK["WATER_TANK_RADIUS"]
    
    WIFI = data['WIFI']
    SSID = WIFI['SSID']
    PASSWORD = WIFI['PASSWORD']
    
    HOTSPOT = data['HOTSPOT']
#     WIFI = data['WIFI']
#     SSID = WIFI['SSID']

    PUMP_RANGE = data["PUMP_RANGE"]
    PUMP_ON_RANGE = PUMP_RANGE["PUMP_ON_RANGE"]
    PUMP_ON_RANGE = range(PUMP_ON_RANGE["LOW"],PUMP_ON_RANGE["HIGH"])
    
    PUMP_OFF_RANGE = PUMP_RANGE["PUMP_OFF_RANGE"]
    PUMP_OFF_RANGE = range(PUMP_OFF_RANGE["LOW"],PUMP_OFF_RANGE["HIGH"])
    
    
    
    ALARM_RANGE = data["ALARM_RANGE"]
    ALARM_ON_RANGE_LOW = ALARM_RANGE["ALARM_ON_RANGE_LOW"]
    ALARM_ON_RANGE_LOW = range(ALARM_ON_RANGE_LOW["LOW"],ALARM_ON_RANGE_LOW["HIGH"])
    
    ALARM_ON_RANGE_FULL = ALARM_RANGE["ALARM_ON_RANGE_FULL"]
    ALARM_ON_RANGE_FULL = range(ALARM_ON_RANGE_FULL["LOW"],ALARM_ON_RANGE_FULL["HIGH"])
    
    
    
    
    PUMP_OFF_RANGE = range(90,101)
    ALARM_ON_RANGE_FULL = range(95, 101)
    ALARM_ON_RANGE_LOW = range(0, 11)



# --------------------------------------------------



#------------------Station config-------------------
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())


#------------------Access Point config-------------------
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid=SSID, password=PASSWORD, authmode=3)
# 
# while ap.active() == False:
#     pass
# 
# print('Connection successful')
# print(ap.ifconfig())


# --------------------------------------------------