#This code was taken from the website: https://www.robotshop.com/en/cytron-13a-5-30v-single-dc-motor-controller.html#description
#This code was provided for the motorcontrollers used for cytron 13A, 5-30V motor controller

import pygame
import RPi.GPIO as GPIO                 # using Rpi.GPIO module
from time import sleep                  # import function sleep for delay
GPIO.setmode(GPIO.BOARD)                  # GPIO numbering
GPIO.setwarnings(False)                 # enable warning from GPIO

# driver number 1 is the right
# driver number 2 is the left
AN2 = 16                                # set pwm2 pin on MD10-Hat
AN1 = 18                                # set pwm1 pin on MD10-hat
DIG2 = 24                               # set dir2 pin on MD10-Hat
DIG1 = 26                               # set dir1 pin on MD10-Hat

RUNSPEED = 40
DELAY = 2
TURN = 35
TRACK_DISTANCE = 0.53			# in METERS

GPIO.setup(AN2, GPIO.OUT)               # set pin as output
GPIO.setup(AN1, GPIO.OUT)               # set pin as output
GPIO.setup(DIG2, GPIO.OUT)              # set pin as output
GPIO.setup(DIG1, GPIO.OUT)              # set pin as output
sleep(1)                                # delay for 1 seconds
p1 = GPIO.PWM(AN1, 100)                 # set pwm for M1
p2 = GPIO.PWM(AN2, 100)                 # set pwm for M2

######################################

DEBOUNCE_INTERVAL = 150

inputPins = [32,22,12,33]
outputPins = [11,13,15,19,21,23,29,31,35,37,40,38,36]

buttons = {1: 32, 2: 22, 3: 12, 4: 33}

global ready
global offset
ready = 0
offset = 1

segToPin = {'la': 15, 'lb': 19, 'lc': 35, 'ld': 13, 'le': 31, 'lf': 11, 'ra': 23, 'rb': 29, 'rc': 36, 'rd': 40, 're': 37, 'rf': 21, 'rg': 38}
disp = {'left':{'0': [segToPin['la'],segToPin['lb'],segToPin['lc'],segToPin['ld'],segToPin['le'],segToPin['lf']],
                '1': [segToPin['lb'],segToPin['lc']],
                '7': [segToPin['la'],segToPin['lb'],segToPin['lc']],
                'u': [segToPin['lb'],segToPin['lc'],segToPin['ld'],segToPin['le'],segToPin['lf']],
                'n': [segToPin['la'],segToPin['lb'],segToPin['lc'],segToPin['le'],segToPin['lf']],
                'blank': [segToPin['la'],segToPin['lb'],segToPin['lc'],segToPin['ld'],segToPin['le'],segToPin['lf']]},
        'right':{'0': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf']],
                '1': [segToPin['rb'],segToPin['rc']],
                '2': [segToPin['ra'],segToPin['rb'],segToPin['rd'],segToPin['re'],segToPin['rg']],
                '3': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['rg']],
                '4': [segToPin['rb'],segToPin['rc'],segToPin['rf'],segToPin['rg']],
                '5': [segToPin['ra'],segToPin['rc'],segToPin['rd'],segToPin['rf'],segToPin['rg']],
                '6': [segToPin['ra'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                '7': [segToPin['ra'],segToPin['rb'],segToPin['rc']],
                '8': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                '9': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rf'],segToPin['rg']],
                'a': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                'b': [segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                'c': [segToPin['ra'],segToPin['rd'],segToPin['re'],segToPin['rf']],
                'd': [segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rg']],
                'e': [segToPin['ra'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                'f': [segToPin['ra'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                'blank': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']]}}


# Name: printSegment
# pos is left right or both displays
# left character (0,1,7,u,n)
# right character (0-9, a-f)
def printSegment(pos, char):
        if(pos == 'both'):
                GPIO.output(disp['left']['blank'], GPIO.LOW)
                GPIO.output(disp['right']['blank'], GPIO.LOW)
                GPIO.output(disp['left'][char[0]], GPIO.HIGH)
                GPIO.output(disp['right'][char[1]], GPIO.HIGH)
        elif(pos == 'left'):
                GPIO.output(disp['left']['blank'], GPIO.LOW)
                GPIO.output(disp['left'][char], GPIO.HIGH)
        elif(pos == 'right'):
                GPIO.output(disp['right']['blank'], GPIO.LOW)
                GPIO.output(disp['right'][char], GPIO.HIGH)


def startButton(channel):
        print("Start Pressed")
        global ready
        ready = 1

def upButton(channel):
        print("Up Pressed")
        global offset
        if(offset < 5):
            offset = offset + 1
            printSegment('both', '0' + str(offset))

def downButton(channel):
        print("Down Pressed")
        global offset
        if(offset > 1):
            offset = offset - 1
            printSegment('both', '0' + str(offset))



######################################
# steer by setting one motor to zero and the other to the 50ish

def stop():
   #print "STOP"
    GPIO.output(DIG1, GPIO.LOW)          # Direction can ignore
    GPIO.output(DIG2, GPIO.LOW)          # Direction can ignore
    p1.start(0)                          # set speed for M1 at 0%
    p2.start(0)                          # set speed for M2 at 0%

## skidSteer ##########################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#
#
#######################################################
def skidSteer(dir, radius, speed, bearing):

    speedOuter = speed * ((radius+TRACK_DISTANCE)/radius)
    if(dir.lower() == "f"):
        #forward
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.HIGH)

        if(int(bearing) >= 0):
            # right or straight
            p1.start(speed) # right side
            p2.start(speed) # left  side

        else:
            # left
            p1.start(speed) # right side
            p2.start(speed) # left  side
    else:
        #backward
        GPIO.output(DIG1, GPIO.HIGH)
        GPIO.output(DIG2, GPIO.LOW)

        if(int(bearing) >= 0): # this one may be backwards
            # right or straight
            p1.start(speed) # right side
            p2.start(speed) # left  side
        else:
            # left
            p1.start(speed) # right side
            p2.start(speed) # left  side

def main():
    GPIO.setup(outputPins, GPIO.OUT) # set all led pins as outputs
    GPIO.setup(inputPins, GPIO.IN, pull_up_down = GPIO.PUD_UP) # set all buttons as inputs with pullup resistors

    GPIO.add_event_detect(buttons[1], GPIO.FALLING, callback=startButton, bouncetime=DEBOUNCE_INTERVAL)
    GPIO.add_event_detect(buttons[2], GPIO.FALLING, callback=upButton, bouncetime=DEBOUNCE_INTERVAL)
    GPIO.add_event_detect(buttons[3], GPIO.FALLING, callback=downButton, bouncetime=DEBOUNCE_INTERVAL)

    printSegment('both', '0' + str(offset))


    try:
        global ready
        global offset
        while True:
            if(ready):
                ready = False
                dir = "F"
                radius = 0.5
                speed = 10 * offset
                bearing = 0
                skidSteer(dir, radius, speed, bearing)
                sleep(2)
                stop()
                sleep(1)

                dir = "R"
                speed = 10 * offset
                skidSteer(dir, radius, speed, bearing)
                sleep(2)
                stop()
                sleep(1)

    except Exception as e:                                 # exit programe when keyboard interupt
        p1.start(0)                          # set speed to 0
        p2.start(0)                          # set speed to 0
        print(e)                                    # Control+x to save file and exit

main()
