from machine import Pin
#We try to disable buzzer as fast as possible as it activates by itself on start
buzzer = Pin(23, Pin.OUT)
buzzer.value(0)
from machine import SoftI2C
from time import sleep_ms, sleep
from imu import MPU6050
import sys
#import mpu6050
import LEDring
import umqtt_robust2
import GPSfunk
#import wifiConnect
import buzzer
import batteryChecker


lib = umqtt_robust2
# opret en ny feed kaldet map_gps indo på io.adafruit
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'mapfeed/csv'), 'utf-8')
# opret en ny feed kaldet speed_gps indo på io.adafruit
speedFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'speedfeed/csv'), 'utf-8')
degreeFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'degreefeed/csv'), 'utf-8')
batteryFeed = bytes('{:s}/feeds/{:s}'.format(b'ingv0351', b'batteryfeed/csv'), 'utf-8')

imu = MPU6050(SoftI2C(scl=Pin(22), sda=Pin(21)))
tickRate = 0
batteryTick = 0
gpsFailTick = 0
gpsFailBool = False
loop = True

# Checks if the MQTT adafruit data have been sent so it can be used with none blocking delays
# Once each packet have been sent it will become True, once everything have been sent it goes back to False
gpsSent = False
speedSent = False
degreeSent = False
batterySent = False

#Controls the tiltTest, activates on green and resets on red
tiltTest = False
tiltTestYellowPass = False

while loop == True:
    if gpsFailBool == True:
        gpsFailTimer +=1
        batteryTick +=1
         
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
          
    #Checks and tries to reconnects to adafruit if a connection issue is present
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            # hvis der forbindes returnere is_conn_issue metoden ingen fejlmeddelse
            lib.c.reconnect()
            pass
        else:
            lib.c.resubscribe()
            pass
    try:
        
        #None blocking delay for GPS publish
        tickRate +=1

        if tickRate >= 1 and tickRate <= 200 and gpsSent == False:
            # print("Number of satalites: " , GPSfunk.numberOfSatallites())
            lib.c.publish(topic=mapFeed, msg=GPSfunk.main())
            print("Gps sent with tickrate: ", tickRate)
            gpsSent = True
        if tickRate >= 201 and tickRate <= 400 and speedSent == False:    
            #print("Speed: ", GPSfunk.main())
            speed = GPSfunk.main()
            speed = speed[:+4]
            print("speed: ",speed)
            lib.c.publish(topic=speedFeed, msg=speed)
            print("speed sent with tickrate: ", tickRate)
            speedSent = True
        if tickRate >= 401 and tickRate <= 600 and degreeSent == False:
            #print(degree)
            lib.c.publish(topic=degreeFeed, msg=str(degree))
            print("Degree sent with tickrate: ", tickRate)
            degreeSent = True
        if tickRate >= 601 and tickRate <= 800 and degreeSent == False:
            print("Trying to send to adafruit with tick: ", tickRate)
            lib.c.publish(topic=batteryFeed, msg=str(batteryChecker.check()))
            print("Battery level sent")
            #Send singal to LED to allot of if statements in LEDring.py
            LEDring.batteryLight(batteryChecker.check())
            batterySent = True
            
        #Checks if True, Resets the packages and tickRate so they are ready to be sent again in order
        if gpsSent and speedSent and degreeSent and batterySent:
            print("Sent messages reseting")
            gpsSent = False
            speedSent = False
            degreeSent = False
            batterySent = False
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
    except TypeError as e:
        print('TypeError: ', e)
    
        
    lib.c.check_msg() # needed when publish(qos=1), ping(), subscribe()
    lib.c.send_queue()  # needed when using the caching capabilities for unsent messages
    
        
lib.c.disconnect()
buzzer.play_error()
    





