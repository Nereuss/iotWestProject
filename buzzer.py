from machine import Pin, PWM
from utime import sleep

buzzer = PWM(Pin(5))
buzzer.freq(500)
buzzer.duty_u16(1000)
sleep(1)
buzzer.duty_u16(0)


# from machine import Pin, PWM
# from utime import sleep
# #We try to disable buzzer as fast as possible
# buzzerOut = Pin(5, Pin.OUT)
# buzzer = PWM(Pin(5))
# 
# 
# # for i in 10:
#     
#     
# buzzerOut.value(0)

# buzzer.freq(500)
#buzzer.freq(1)
# buzzer.duty_u16(1000)
#sleep(1)
# buzzer.value(0)