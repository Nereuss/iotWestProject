import machine
from machine import Pin
from machine import ADC
from time import sleep_ms, sleep

# Battery Voltage ADC
# batmult = 1.64
#batmult = 1.78
#batmult = 3.938
batmult = 1

vdcmult = 1.774

battadc = ADC(Pin(34))

battadc.atten(ADC.ATTN_11DB)

def check():
    bat_vdc = round((battadc.read()/1000) * (batmult), 3)
    vdc_calc = round(bat_vdc * vdcmult, 3)
    return vdc_calc
    

# while True:
#     sleep(1)
#     print(check())
#     bat_vdc = round((battadc.read()/1000) * (batmult), 2)
#     bat_final = bat_vdc * 2
#     #print(battadc.read())
#     print(bat_vdc , " ADC value: ", battadc.read())
#     #print(bat_final)