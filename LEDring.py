from time import sleep
from machine import UART, Pin
import sys
import neopixel
import random
import time 

n = 12
p = 15
p2 = 17



np = neopixel.NeoPixel(Pin(p), n)
np2 = neopixel.NeoPixel(Pin(p2), n)

#Gives place holder first LED as np but can also accept np2 for second LED
def set_color(r,g,b, np = np):
    for i in range(n):
        np[i] = (r,g,b)
    np.write()

def clear(np = np):
    for i in range(n):
        np[i] = (0,0,0, 128)
        np.write()

def yellow(np = np):
    for i in range(n):
        np[i] = (100,50,0, 128)
        np.write()

def green(np = np):
    for i in range(n):
        np[i] = (0,100,0, 128)
        np.write()

def red(np = np):
    for i in range(n):
        np[i] = (100,0,0, 128)
        np.write()
        
def white(np = np):
    for i in range(n):
        np[i] = (100,100,100, 128)
        np.write()
        
def doubleWhiteBlink(np = np):
    white()
    sleep(0.3)
    clear()
    sleep(0.3)
    white()
    sleep(0.3)
    clear()
    
def doubleRedBlink(np = np):
    red()
    sleep(0.3)
    clear()
    sleep(0.3)
    red()
    sleep(0.3)
    clear()

def bounce(r=1,g=5,b=1,wait=1):
    for i in range(1*n):
        for j in range(n):
            np[j] = (r,g,b, 1)
        if (i // n) % 2 == 0:
            np[i % n] = (0,0,0, 1)
        np.write()
        sleep(wait)
        
def fadeLight(np = np):
    # fade in/out
    for i in range(0, 4 * 256, 2):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()
        
 
# Control the back LED to display battery level 
def lightController(r,g,b, batRange):
    clear(np2)
    for i in range(batRange):
        np2[i] = (r,g,b, 128)
        np2.write() 

#Fade light on back LED until changed
fadeLight(np2)
        
# lightController(0,50,0,3)

# Displays the battery percentage in 12 sections
# green full to almost full, yellow medium full, red almost empty
def batteryLight(batCharge):
    if batCharge >= 8.18:
        lightController(0,50,0,12)
    if batCharge >= 7.98 and batCharge <= 8.179:
        lightController(0,50,0,11)
    if batCharge >= 7.82 and batCharge <= 7.979:
        lightController(0,50,0,10)
    if batCharge >= 7.69 and batCharge <= 7.819:
        lightController(0,50,0,9)
    if batCharge >= 7.59 and batCharge <= 7.689:
        lightController(50,25,0,8)
    if batCharge >= 7.53 and batCharge <= 7.589:
        lightController(50,25,0,7)
    if batCharge >= 7.51 and batCharge <= 7.529:
        lightController(50,25,0,6)
    if batCharge >= 7.45 and batCharge <= 7.509:
        lightController(50,25,0,5)
    if batCharge >= 7.37 and batCharge <= 7.449:
        lightController(50,0,0,4)
    if batCharge >= 7.23 and batCharge <= 7.369:
        lightController(50,0,0,3)
    if batCharge >= 6.98 and batCharge <= 7.229:
        lightController(50,0,0,2)
    if batCharge <= 6.98:
        lightController(50,0,0,1)
        
    
    
        
        