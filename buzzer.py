# How to make some sound with MicroPython
# Example 2: Make a mario sound
# Author: George Bantique,
#         TechToTinker Youtube channel
#		  techtotinker.blogspot.com
# Date: September 18, 2020
# https://techtotinker.blogspot.com/2020/09/007-micropython-tutorial-how-to-make.html
# https://github.com/james1236/buzzer_music/blob/main/example.py

import machine
import time
from math import ceil
from machine import Pin
from buzzer_music import music


p23 = machine.Pin(23, machine.Pin.OUT)

# These are the notes with equivalent frequency
# https://www.blackghostaudio.com/blog/basic-music-theory-for-beginners
B0  = 31
C1  = 33
CS1 = 35
D1  = 37
DS1 = 39
E1  = 41
F1  = 44
FS1 = 46
G1  = 49
GS1 = 52
A1  = 55
AS1 = 58
B1  = 62
C2  = 65
CS2 = 69
D2  = 73
DS2 = 78
E2  = 82
F2  = 87
FS2 = 93
G2  = 98
GS2 = 104
A2  = 110
AS2 = 117
B2  = 123
C3  = 131
CS3 = 139
D3  = 147
DS3 = 156
E3  = 165
F3  = 175
FS3 = 185
G3  = 196
GS3 = 208
A3  = 220
AS3 = 233
B3  = 247
C4  = 262
CS4 = 277
D4  = 294
DS4 = 311
E4  = 330
F4  = 349
FS4 = 370
G4  = 392
GS4 = 415
A4  = 440
AS4 = 466
B4  = 494
C5  = 523
CS5 = 554
D5  = 587
DS5 = 622
E5  = 659
F5  = 698
FS5 = 740
G5  = 784
GS5 = 831
A5  = 880
AS5 = 932
B5  = 988
C6  = 1047
CS6 = 1109
D6  = 1175
DS6 = 1245
E6  = 1319
F6  = 1397
FS6 = 1480
G6  = 1568
GS6 = 1661
A6  = 1760
AS6 = 1865
B6  = 1976
C7  = 2093
CS7 = 2217
D7  = 2349
DS7 = 2489
E7  = 2637
F7  = 2794
FS7 = 2960
G7  = 3136
GS7 = 3322
A7  = 3520
AS7 = 3729
B7  = 3951
C8  = 4186
CS8 = 4435
D8  = 4699
DS8 = 4978


# Function play is use to play sound from a list of notes
def play(pin, melodies, delays, duty):
	# Create the pwm object
    pwm = machine.PWM(pin)
    # Loop through the whole list
    for note in melodies:
        pwm.freq(note)
        pwm.duty(duty)
        time.sleep(delays)
    # Disable the pulse, setting the duty to 0
    pwm.duty(0)
    # Disconnect the pwm driver
    pwm.deinit()

# This is the list of notes for mario theme
# 0 denotes rest notes
mario = [
     E7, E7,  0, E7,  0, C7, E7,  0,
     G7,  0,  0,  0, G6,  0,  0,  0,
     C7,  0,  0, G6,  0,  0, E6,  0,
      0, A6,  0, B6,  0,AS6, A6,  0,
     G6, E7,  0, G7, A7,  0, F7, G7,
      0, E7,  0, C7, D7, B6,  0,  0,
     C7,  0,  0, G6,  0,  0, E6,  0,
      0, A6,  0, B6,  0,AS6, A6,  0,
     G6, E7,  0, G7, A7,  0, F7, G7,
      0, E7,  0, C7, D7, B6,  0,  0,
]
jingle = [
    E7, E7, E7, 0,
    E7, E7, E7, 0,
    E7, G7, C7, D7, E7, 0,
    F7, F7, F7, F7, F7, E7, E7, E7, E7, D7, D7, E7, D7, 0, G7, 0,
    E7, E7, E7, 0,
    E7, E7, E7, 0,
    E7, G7, C7, D7, E7, 0,
    F7, F7, F7, F7, F7, E7, E7, E7, G7, G7, F7, D7, C7, 0 
]
twinkle = [
    C6, C6, G6, G6, A6, A6, G6, 0,
    F6, F6, E6, E6, D6, D6, C6, 0,
    G6, G6, F6, F6, E6, E6, D6, 0,
    G6, G6, F6, F6, E6, E6, D6, 0,
    C6, C6, G6, G6, A6, A6, G6, 0,
    F6, F6, E6, E6, D6, D6, C6, 0,
]

startup = [
    AS7, 0, A1, 0, D8 ,  
]

error = [
    F2, 0, F2,  
]

errorInternet = [
    B3, 0, B2, B2, F5, 0, B3 
]

closeDown = [
    # C7,  0,  0, G6,  0,  0, E6,  0,
    G6, E7,  0, G7, A7,  0, F7, G7,
]

tiltTest = [
    E7, C7
]



# Function to easily play the mario theme
def play_mario():
    # Play the mario theme to GPIO 23
    # with 150ms note interval
    # with a low volume
    play(p23, mario, 0.15, 50)

def play_twinkle():
    play(p23, twinkle, 0.15, 50)
    
def play_jingle():
    play(p23, jingle, 0.15, 50)

def play_startup():
    play(p23, startup, 0.15, 50)
    
def play_closeDown():
    play(p23, closeDown, 0.15, 50)

def play_error():
    play(p23, error, 0.15, 50)

def play_error_noInternet():
    play(p23, errorInternet, 0.15, 50)

def play_tiltTest():
    play(p23, tiltTest, 0.15, 100) 
    
# play(p23, jingle, 0.15, 50)

# song = '0 A#3 1 0;0 F#3 2 0;1 C#4 1 0;2 C4 1 0;3 C#4 1 0;4 A#3 1 0;6 A#3 1 0;6 F#3 2 0;7 C4 1 0;8 C#4 1 0;9 G#4 1 0;10 F4 1 0;12 A#3 1 0;12 F#3 2 0;13 C#4 1 0;14 C4 1 0;15 C#4 1 0;16 A#3 1 0;18 A#3 1 0;18 F#3 2 0;19 C4 1 0;20 C#4 1 0;21 G#4 1 0;22 F4 1 0;24 A#3 1 0;24 F3 2 0;25 C#4 1 0;26 C4 1 0;27 C#4 1 0;28 A#3 1 0;30 A#3 1 0;31 C4 1 0;30 F3 2 0;32 C#4 1 0;33 G#4 1 0;34 F4 1 0;36 F3 2 0;36 D#5 2 0;38 C6 2 0;38 G#3 2 0;40 C4 2 0;40 A#5 2 0;42 G#5 1 0;42 D#4 2 0;43 F#5 1 0;44 C4 1 0;45 G#3 1 0;44 F5 2 0;46 D#4 1 0;47 C4 1 0;46 G#5 2 0;48 A#3 1 0;48 F#3 2 0;49 C#4 1 0;50 C4 1 0;51 C#4 1 0;52 A#3 1 0;54 A#3 1 0;55 C4 1 0;54 F#3 2 0;56 C#4 1 0;57 G#4 1 0;58 F4 1 0;60 A#3 1 0;60 F#3 2 0;61 C#4 1 0;48 A#5 15 0;62 C4 1 0;63 C#4 1 0;64 A#3 1 0;66 A#3 1 0;66 F#3 2 0;67 C4 1 0;68 C#4 1 0;69 G#4 1 0;70 F4 1 0;72 A#3 1 0;72 F3 2 0;73 C#4 1 0;74 C4 1 0;75 C#4 1 0;76 A#3 1 0;78 A#3 1 0;78 F3 2 0;79 C4 1 0;80 C#4 1 0;81 G#4 1 0;82 F4 1 0;84 D#5 2 0;84 D#6 2 0;84 G#3 2 0;86 C7 2 0;86 D#3 2 0;86 C6 2 0;88 A#6 2 0;88 F3 2 0;88 A#5 2 0;90 G#5 1 0;90 G#6 1 0;90 G#3 2 0;91 F#6 1 0;91 F#5 1 0;92 F5 2 0;92 C4 2 0;92 F6 2 0;94 D#4 2 0;94 G#6 2 0;94 G#5 2 0;96 F#3 2 0;98 C4 1 0;99 C#4 1 0;100 A#3 1 0;101 F3 1 0;96 A#5 8 0;102 F#3 2 0;104 C4 1 0;104 F5 2 0;105 C#4 1 0;106 A#3 1 0;106 G#5 2 0;107 D#4 1 0;108 G#3 2 0;110 D#3 1 0;108 A#5 4 0;111 F3 1 0;112 G#3 1 0;112 C#6 2 0;113 F3 1 0;114 D#6 1 0;114 D#3 2 0;115 C#6 1 0;116 F3 2 0;116 C6 2 0;118 G#3 2 0;118 C#6 2 0;120 A#3 1 0;121 A#4 1 0;122 D#4 1 0;123 F4 1 0;124 C#4 1 0;125 G#3 1 0;126 A#3 1 0;127 A#4 1 0;128 D#4 1 0;129 F4 1 0;130 C#4 1 0;131 G#3 1 0;132 A#3 1 0;133 A#4 1 0;120 A#5 15 0;134 D#4 1 0;135 F4 1 0;136 C#4 1 0;137 F3 1 0;138 G#3 2 0;140 D#3 2 0;142 G#3 2 0;144 A#4 1 0;144 A#3 1 0;144 F#3 1 0;145 C#5 1 0;145 C#4 1 0;146 C5 1 0;146 C4 1 0;147 C#5 1 0;147 C#4 1 0;148 A#4 1 0;148 A#3 1 0;150 A#4 1 0;150 F#3 1 0;150 A#3 1 0;151 C4 1 0;151 C5 1 0;152 C#4 1 0;152 C#5 1 0;153 G#4 1 0;154 F4 1 0;154 F5 1 0;156 A#4 1 0;156 A#3 1 0;156 F#3 1 0;157 C#5 1 0;157 C#4 1 0;158 C5 1 0;158 C4 1 0;159 C#5 1 0;159 C#4 1 0;160 A#3 1 0;160 A#4 1 0;162 A#4 1 0;162 A#3 1 0;162 F#3 1 0;163 C5 1 0;163 C4 1 0;164 C#5 1 0;164 C#4 1 0;165 G#4 1 0;166 F5 1 0;166 F4 1 0;168 A#3 1 0;168 F3 1 0;168 A#4 1 0;169 C#5 1 0;169 C#4 1 0;170 C5 1 0;170 C4 1 0;171 C#4 1 0;171 C#5 1 0;172 A#3 1 0;172 A#4 1 0;174 A#4 1 0;174 A#3 1 0;174 F3 1 0;175 C5 1 0;175 C4 1 0;176 C#5 1 0;176 C#4 1 0;177 G#4 1 0;178 F4 1 0;178 F5 1 0;180 F3 2 0;180 D#6 2 0;180 F4 2 0;182 G#4 2 0;182 C7 2 0;182 G#3 2 0;184 C4 2 0;184 A#6 2 0;184 C5 2 0;186 G#6 1 0;186 D#5 2 0;186 D#4 2 0;187 F#6 1 0;188 C5 1 0;188 C4 1 0;189 G#3 1 0;189 G#4 1 0;188 F6 2 0;190 D#4 1 0;190 D#5 1 0;191 C5 1 0;190 G#6 2 0;191 C4 1 0;192 A#4 1 0;192 A#3 1 0;192 F#3 1 0;193 C#5 1 0;193 C#4 1 0;194 C4 1 0;194 C5 1 0;195 C#4 1 0;195 C#5 1 0;196 A#4 1 0;196 A#3 1 0;198 F#3 1 0;198 A#3 1 0;198 A#4 1 0;199 C5 1 0;199 C4 1 0;200 C#4 1 0;200 C#5 1 0;201 G#4 1 0;202 F4 1 0;202 F5 1 0;204 A#4 1 0;204 F#3 1 0;204 A#3 1 0;205 C#4 1 0;205 C#5 1 0;206 C5 1 0;192 A#6 15 0;206 C4 1 0;207 C#4 1 0;207 C#5 1 0;208 A#3 1 0;208 A#4 1 0;210 A#3 1 0;210 F#3 1 0;210 A#4 1 0;211 C5 1 0;211 C4 1 0;212 C#5 1 0;212 C#4 1 0;213 G#4 1 0;214 F5 1 0;214 F4 1 0;216 D#5 1 0;216 D#4 1 0;217 F4 1 0;217 F5 1 0;218 G#5 1 0;218 G#4 1 0;219 A#4 1 0;219 A#5 1 0;220 C6 1 0;220 C5 1 0;221 C#6 1 0;221 C#5 1 0;222 D#6 1 0;222 D#5 1 0;223 C#6 1 0;223 C#5 1 0;224 C6 1 0;224 C5 1 0;225 A#5 1 0;225 A#4 1 0;226 G#5 1 0;226 G#4 1 0;227 F4 1 0;227 F5 1 0;228 G#5 2 0;228 G#4 2 0;228 D#6 2 0;228 G#3 2 0;230 C7 2 0;230 D#3 2 0;230 D#4 2 0;230 D#6 2 0;232 F4 2 0;232 C#6 2 0;232 F3 2 0;232 A#6 2 0;234 G#6 1 0;234 C6 1 0;234 G#3 2 0;234 G#4 2 0;235 A#5 1 0;235 F#6 1 0;236 G#5 2 0;236 F6 2 0;236 C5 2 0;236 C4 2 0;238 G#6 2 0;238 F5 2 0;238 D#4 2 0;238 D#5 2 0;240 F#3 2 0;242 C4 1 0;243 C#4 1 0;244 A#3 1 0;245 F3 1 0;240 A#5 8 0;246 F#3 2 0;240 F#5 8 0;248 C4 1 0;248 F5 2 0;248 C5 2 0;249 C#4 1 0;250 A#3 1 0;250 G#5 2 0;250 D#5 2 0;251 D#4 1 0;252 G#3 2 0;254 D#3 1 0;252 F5 4 0;252 A#5 4 0;255 F3 1 0;256 G#3 1 0;256 F5 2 0;256 C#6 2 0;257 F3 1 0;258 F#5 1 0;258 D#6 1 0;258 D#3 2 0;259 C#6 1 0;259 F5 1 0;260 D#5 2 0;260 C6 2 0;260 F3 2 0;262 G#3 2 0;262 C#6 2 0;262 F5 2 0;264 A#3 1 0;265 A#4 1 0;266 D#4 1 0;267 F4 1 0;268 C#4 1 0;269 G#3 1 0;270 A#3 1 0;271 A#4 1 0;272 D#4 1 0;273 F4 1 0;274 C#4 1 0;275 G#3 1 0;276 A#3 1 0' 
# mySong = music(song, pins=[Pin(23)])
# 
# while True:
#     print(mySong.tick())
#     sleep(0.04)

