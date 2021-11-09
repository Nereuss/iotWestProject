from machine import Pin
#We try to disable buzzer as fast as possible
buzzer = Pin(5, Pin.OUT)
buzzer.value(0)
from machine import SoftI2C
from time import sleep_ms, sleep
import sys
import mpu6050
import LEDring
import umqtt_robust2
import GPSfunk
import wifiConnect

lib = umqtt_robust2
# opret en ny feed kaldet map_gps indo på io.adafruit
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'mapfeed/csv'), 'utf-8')
# opret en ny feed kaldet speed_gps indo på io.adafruit
speedFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'speedfeed/csv'), 'utf-8')
accXFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'accXfeed/csv'), 'utf-8')
accYFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'accYfeed/csv'), 'utf-8')
accZFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'accZfeed/csv'), 'utf-8')


i2c = SoftI2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266
mpu= mpu6050.accel(i2c)

# wifiConnect.connect()
# LEDring.bounce()
# LEDring.demo()

# mpu.get_values()

# print(mpu.get_values()["AcX"])







loop = True
while loop == True:
    LEDring.fadeLight()
#     gyro = mpu.get_values()
    print(mpu.get_values())
    velocityZ = mpu.get_values()["AcZ"]
    velocityX = mpu.get_values()["AcX"]
    velocityY = mpu.get_values()["AcY"]
    #velocityY = mpu.get_values()["AcY"]*0.0001*9.8
#         print("Velocity Z: " + str(velocityZ) + " -  Velocity X: "+ str(velocityX) + " - Velocity Y: " + str(velocityY))
        # sleep(500)
    
    
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            # hvis der forbindes returnere is_conn_issue metoden ingen fejlmeddelse
            lib.c.reconnect()
            pass
        else:
            lib.c.resubscribe()
            pass
    try:
        lib.c.publish(topic=mapFeed, msg=GPSfunk.main())
        speed = GPSfunk.main()
        speed = speed[:4]
        print("speed: ",speed)
        lib.c.publish(topic=speedFeed, msg=speed)
        lib.c.publish(topic=accXfeed, msg=bytes(velocityX))
        lib.c.publish(topic=accYfeed, msg=bytes(velocityY))
        lib.c.publish(topic=accZfeed, msg=bytes(velocityZ))
        sleep(10)
        
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        lib.c.disconnect()
        lib.wifi.active(False)
        lib.sys.exit()
    except OSError as e:
        print('Failed to read sensor.')
        
    except NameError as e:
        print('NameError')
        
    except TypeError as e:
        print('TypeError')
        
    lib.c.check_msg() # needed when publish(qos=1), ping(), subscribe()
    lib.c.send_queue()  # needed when using the caching capabilities for unsent messages
    
#     try:
#         # LEDring.demo(LEDring.np)
#         gyro = mpu.get_values()
#         # print(mpu.get_values())
#         velocityZ = mpu.get_values()["AcZ"]*0.0001*9.8
#         velocityX = mpu.get_values()["AcX"]*0.0001*9.8
#         velocityY = mpu.get_values()["AcY"]*0.0001*9.8
#         print("Velocity Z: " + str(velocityZ) + " -  Velocity X: "+ str(velocityX) + " - Velocity Y: " + str(velocityY))
#         # sleep(500)
#         pass
#              
#     except KeyboardInterrupt:
#         print("Exiting")
#         loop = False
#         sleep(5)
#         sys.exit
        
lib.c.disconnect()
    





