import machine
from machine import Pin
from machine import ADC
from time import sleep_ms, sleep

# Battery Voltage ADC
# batmult = 1.64
batmult = 1.78
battadc = ADC(Pin(36))

battadc.atten(ADC.ATTN_11DB)    # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
#battadc.width(ADC.WIDTH_9BIT)   # set 9 bit return values (returned range 0-511)
                # read value using the newly configured attenuation and width


# bat_pin = battadc.channel(pin='P36', attn=ADC.ATTN_11DB)
# 
# 
# def getBatt():
#     pycom.rgbled(0x0A0F00)                        # Mid Orange
#     bat_vdc = round((bat_pin()/1000) * (batmult), 2)
#     if bat_vdc <= 3.40:
#         lowBatt(bat_vdc)
#         battIS = 1
# 
#     else: battIS = 0
# 
#     utime.sleep(0.1)
#     pycom.rgbled(0x000000)
#     return battIS, bat_vdc

# vcc = machine.ADC(36)
# vcc.read()

while True:
    sleep(1)
    bat_vdc = round((battadc.read()/1000) * (batmult), 2)
    bat_final = bat_vdc * 2
    #print(battadc.read())
    print(bat_vdc , " ADC value: ", battadc.read())
    #print(bat_final)