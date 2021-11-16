from machine import Pin
#We try to disable buzzer as fast as possible as it activates by itself on start
buzzer = Pin(5, Pin.OUT)
buzzer.value(0)
from machine import SoftI2C
from time import sleep_ms, sleep
from imu import MPU6050
import sys
import mpu6050
import LEDring
import umqtt_robust2
import GPSfunk
import wifiConnect
import buzzer


lib = umqtt_robust2
# opret en ny feed kaldet map_gps indo på io.adafruit
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'mapfeed/csv'), 'utf-8')
# opret en ny feed kaldet speed_gps indo på io.adafruit
speedFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'speedfeed/csv'), 'utf-8')
degreeFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'degreefeed/csv'), 'utf-8')


# i2c = SoftI2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266


# wifiConnect.connect()
# LEDring.bounce()
# LEDring.demo()

# mpu.get_values()

# print(mpu.get_values()["AcX"])




imu = MPU6050(SoftI2C(scl=Pin(22), sda=Pin(21)))
tickRate = 0
loop = True

# Checks if the MQTT adafruit data have been sent so it can be used with none blocking delays
# Once each packet have been sent it will become True, once everything have been sent it goes back to False
gpsSent = False
speedSent = False
degreeSent = False

#Controls the tiltTest, activates on green and resets on red
tiltTest = False
tiltTestYellowPass = False

while loop == True:
    degree = imu.accel.z * 90 + 90
    
    if degree >= 40 and degree <= 70:
        LEDring.yellow()
        if tiltTest == True:
            if tiltTestYellowPass == False:
                tiltTestYellowPass = True
                
    if degree >= 20 and degree <= 39:
        LEDring.green()
        if tiltTest == False:
            buzzer.play_tiltTest()        
            tiltTest = True
            
    if degree >= 70 and degree <= 180:
        LEDring.red()
        #If both are true
        if tiltTestYellowPass and tiltTest:
            tiltTestYellowPass = False
            tiltTest = False
            
            
        
    #if degree <= 20 or degree <= 180:
        # LEDring.red()
    # LEDring.green()
    # LEDring.fadeLight()
#   gyro = mpu.get_values()
    # print(mpu.get_values())

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
        #sleep(4)
#         tickRate +=1
#         if tickRate >= 1000:
        # print("test start")
        
        #None blocking delay for GPS publish
        tickRate +=1
        #print(tickRate)
        
        if tickRate >= 1 and tickRate <= 150 and gpsSent == False:
            # print("Number of satalites: " , GPSfunk.numberOfSatallites())
            lib.c.publish(topic=mapFeed, msg=GPSfunk.main())
            print("Gps sent with tickrate: ", tickRate)
            gpsSent = True
        if tickRate >= 151 and tickRate <= 300 and speedSent == False:    
            #print("Speed: ", GPSfunk.main())
            speed = GPSfunk.main()
            speed = speed[:+4]
            print("speed: ",speed)
            lib.c.publish(topic=speedFeed, msg=speed)
            print("speed sent with tickrate: ", tickRate)
            speedSent = True
        if tickRate >= 301 and tickRate <= 450 and degreeSent == False:
            #print(degree)
            lib.c.publish(topic=degreeFeed, msg=str(degree))
            print("Degree sent with tickrate: ", tickRate)
            degreeSent = True
        #Checks if True, Resets the packages and tickRate so they are ready to be sent again in order
        if gpsSent and speedSent and degreeSent:
            print("Sent messages reseting")
            gpsSent = False
            speedSent = False
            degreeSent = False
            tickRate = 0
            
        
        
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
    #except TypeError as e:
    #    print('TypeError: ', e)
    
        
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
buzzer.play_error()
    





