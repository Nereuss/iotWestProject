from time import sleep
from machine import UART, Pin
import sys
import neopixel
import random
import time 

n = 12
p = 15

np = neopixel.NeoPixel(Pin(p), n)

np[0] = (255, 0, 0, 1)
np[3] = (125,  204, 223, 1)
np[7] = (120, 153, 23, 1)
np[10] = (255, 0, 153, 1)

def set_color(r,g,b):
    for i in range(n):
        np[i] = (r,g,b)
    np.write()

def clear():
    for i in range(n):
        np[i] = (0,0,0, 128)
        np.write()

def yellow():
    for i in range(n):
        np[i] = (100,50,0, 128)
        np.write()

def green():
    for i in range(n):
        np[i] = (0,100,0, 128)
        np.write()

def red():
    for i in range(n):
        np[i] = (100,0,0, 128)
        np.write()
        
def white():
    for i in range(n):
        np[i] = (100,100,100, 128)
        np.write()
        
def doubleWhiteBlink():
    white()
    sleep(0.3)
    clear()
    sleep(0.3)
    white()
    sleep(0.3)
    clear()
    
def doubleRedBlink():
    red()
    sleep(0.3)
    clear()
    sleep(0.3)
    red()
    sleep(0.3)
    clear()




def demo(np = np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()



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



# while True:
#     sleep(0.1)
#     demo(np)
    #bounce(random.randint(1, 222),random.randint(1, 2),random.randint(1, 2),0.019)
    #set_color(random.randint(1, 255),random.randint(1, 255),random.randint(1, 255))

#np.write()
#sleep(10)
#clear()

###### MP3 player #######

uart1 = UART(1, baudrate=9600, tx=16, rx=17)
# STARTBYTE, VER, Len, CMD, FEEDBACK, PARA1, PARA2, PARA3, PARA4, CHECKSUM, ENDBYTE
play = bytes([0x7E, 0xFF, 0x06, 0x0D, 0x00, 0x00, 0x01, 0xFE, 0xED, 0xEF])
pause = bytes([0x7E, 0xFF, 0x06, 0x0E, 0x00, 0x00, 0x00, 0xFE, 0xED, 0xEF])
volume10 = bytes([0x7E, 0xFF, 0x06, 0x06, 0x00, 0x00, 0x10, 0xFE, 0xE5, 0xEF])
volume15 = bytes([0x7E, 0xFF, 0x06, 0x06, 0x00, 0x00, 0x15, 0xFE, 0xE0, 0xEF])
volume20 = bytes([0x7E, 0xFF, 0x06, 0x06, 0x00, 0x00, 0x20, 0xFE, 0xD5, 0xEF])

track1 = bytes([0x7E, 0xFF, 0x06, 0x12, 0x00, 0x00, 0x01, 0xFE, 0xE8, 0xEF])
track2 = bytes([0x7E, 0xFF, 0x06, 0x12, 0x00, 0x00, 0x02, 0xFE, 0xE7, 0xEF])
track3 = bytes([0x7E, 0xFF, 0x06, 0x12, 0x00, 0x00, 0x03, 0xFE, 0xE6, 0xEF])
track4 = bytes([0x7E, 0xFF, 0x06, 0x12, 0x00, 0x00, 0x04, 0xFE, 0xE5, 0xEF])
track5 = bytes([0x7E, 0xFF, 0x06, 0x12, 0x00, 0x00, 0x05, 0xFE, 0xE4, 0xEF])
track6 = bytes([0x7E, 0xFF, 0x06, 0x12, 0x00, 0x00, 0x06, 0xFE, 0xE3, 0xEF])

# uart1.write(volume10)
# while True:
#     try:
#         print("UART1")
#         uart1.write(track1) # write 5 bytes
#         sleep(20)
#  # Stopper programmet når der trykkes Ctrl + c
#     except KeyboardInterrupt:
#         print('Ctrl-C pressed...exiting')
#         sleep(5)
#         sys.exit()