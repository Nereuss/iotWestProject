import utime

import sys
import network
import os
import buzzer
import LEDring

sys.path.insert(1, '/path/to/application/app/folder')
from umqtt.robust2 import MQTTClient

try:
    from credentials import credentials
except ImportError:
    print("Credentials are kept in credentials.py, please add them there!")
    raise
# WiFi connection information
#WIFI_SSID = credentials["ssid"]
#WIFI_PASSWORD = credentials["password"]

# WIFI_SSID = "esp32Lab"
# WIFI_PASSWORD = "Lab3004#"
WIFI_SSID = "LTE-1998"
WIFI_PASSWORD = "12345678"

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print(WIFI_SSID + " " + WIFI_PASSWORD)






def connect():
    try:
        if not wifi.isconnected():
            wifi.disconnect()
            print("Connecting to network...")
            wifi.connect(WIFI_SSID, WIFI_PASSWORD)              
        while not wifi.isconnected():
            pass
        print("network config: ", wifi.ifconfig())
        buzzer.play_startup()
        LEDring.doubleWhiteBlink()
    except:
        print("Connection Error")
        buzzer.play_error()
        LEDring.doubleRedBlink()
        
connect()
# wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
# while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
#     attempt_count += 1
#     utime.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()
besked = ""
def sub_cb(topic, msg, retained, duplicate):
    #print((topic, msg, retained, duplicate))
    m = msg.decode('utf-8')
    global besked
    besked = m.lower()
    print(besked)
# create a random MQTT clientID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

# connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
#
# To use a secure connection (encrypted) with TLS:
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses about 9k bytes of the heap
#         (about 1/4 of the micropython heap on the ESP8266 platform)
ADAFRUIT_IO_URL = credentials["ADAFRUIT_IO_URL"]
ADAFRUIT_USERNAME = credentials["ADAFRUIT_USERNAME"]
ADAFRUIT_IO_KEY = credentials["ADAFRUIT_IO_KEY"]
ADAFRUIT_IO_PUB_FEEDNAME = credentials["ADAFRUIT_IO_PUB_FEEDNAME"]
ADAFRUIT_IO_SUB_FEEDNAME = credentials["ADAFRUIT_IO_SUB_FEEDNAME"]

c = MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
# Print diagnostic messages when retries/reconnects happens
c.DEBUG = True
# Information whether we store unsent messages with the flag QoS==0 in the queue.
c.KEEP_QOS0 = False
# Option, limits the possibility of only one unique message being queued.
c.NO_QUEUE_DUPS = True
# Limit the number of unsent messages in the queue.
c.MSG_QUEUE_MAX = 2

c.set_callback(sub_cb)

mqtt_pub_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_PUB_FEEDNAME), 'utf-8')
mqtt_sub_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_SUB_FEEDNAME), 'utf-8')
if not c.connect(clean_session=False):
    print("New session being set up")
    c.subscribe(mqtt_sub_feedname)