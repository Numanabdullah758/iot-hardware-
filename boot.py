#hehehehehe
import usocket as socket
import network
import math

from machine import Pin, ADC ,Timer
#import machine
from constants import *
from time import sleep

from hcsr04 import HCSR04

import onewire, ds18x20
import dht

import esp
esp.osdebug(None)

import gc
gc.collect()

#-------------------All Sensor----------------------
jsn_sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)


esp_led = Pin(ESP_LED_PIN,Pin.OUT)

relay1 = Pin(RELAY_1_PIN,Pin.OUT)
relay2 = Pin(RELAY_2_PIN,Pin.OUT)
relay3 = Pin(RELAY_3_PIN,Pin.OUT)
relay4 = Pin(RELAY_4_PIN,Pin.OUT)

relay1.value(not False)
relay2.value(not False)
relay3.value(not False)
relay4.value(not False)

#------------------Station config-------------------
#station = network.WLAN(network.STA_IF)
#station.active(True)
#station.connect(SSID, PASSWORD)

#while station.isconnected() == False:
#    pass

#print('Connection successful')
#print(station.ifconfig())


#------------------Access Point config-------------------
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID, password=PASSWORD, authmode=3)

while ap.active() == False:
    pass

print('Connection successful')
print(ap.ifconfig())

