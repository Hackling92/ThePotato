#This code was taken from the website: https://www.robotshop.com/en/cytron-13a-5-30v-single-dc-motor-controller.html#description
#This code was provided for the motorcontrollers used for cytron 13A, 5-30V motor controller


#import pygame
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

RUNSPEED = 10
DELAY = 2
TURN = 8

GPIO.setup(AN2, GPIO.OUT)               # set pin as output
GPIO.setup(AN1, GPIO.OUT)               # set pin as output
GPIO.setup(DIG2, GPIO.OUT)              # set pin as output
GPIO.setup(DIG1, GPIO.OUT)              # set pin as output
sleep(1)                                # delay for 1 seconds
p1 = GPIO.PWM(AN1, 100)                 # set pwm for M1
p2 = GPIO.PWM(AN2, 100)                 # set pwm for M2


# steer by setting one motor to zero and the other to the 50ish

## fullStop ########################################### 
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#
#
#######################################################
def fullStop():
    print("    Full-Stop")
    GPIO.output(DIG1, GPIO.LOW)          # Direction can ignore
    GPIO.output(DIG2, GPIO.LOW)          # Direction can ignore
    p1.start(0)                          # set speed for M1 at 0%
    p2.start(0)                          # set speed for M2 at 0%
    #sleep(DELAY)                        # delay for 3 second
    return 0

## forward ############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#
#
#######################################################
def forward():
    print("    Forward")
    GPIO.output(DIG1, GPIO.HIGH)          # set DIG1 as LOW, to control direction
    GPIO.output(DIG2, GPIO.HIGH)          # set DIG2 as LOW, to control direction
    p1.start(RUNSPEED)                        # set speed for M1 at 100%   
    p2.start(RUNSPEED)
    #sleep(DELAY)                             #delay for 2 second
    return 0

## forwardLeft ############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#
#
#######################################################
def forwardLeft():
    print("    Forward-Left")
    GPIO.output(DIG1, GPIO.HIGH)          # set DIG1 as LOW, to control direction
    GPIO.output(DIG2, GPIO.HIGH)          # set DIG2 as LOW, to control direction
    p1.start(RUNSPEED)                        # set speed for M1 at 100%   
    p2.start(RUNSPEED - TURN)
    #sleep(DELAY)                             #delay for 2 second
    return 0

## forwardRight #######################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#
#
#######################################################
def forwardRight():
    print("    Forward-Right")
    GPIO.output(DIG1, GPIO.HIGH)          # set DIG1 as LOW, to control direction
    GPIO.output(DIG2, GPIO.HIGH)          # set DIG2 as LOW, to control direction
    p1.start(RUNSPEED - TURN)                        # set speed for M1 at 100%   
    p2.start(RUNSPEED)
    #sleep(DELAY)                             #delay for 2 second
    return 0

## reverse ############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#
#
#######################################################
def reverse():
    print("    Reverse")
    GPIO.output(DIG1, GPIO.LOW)         # set DIG1 as HIGH, to control direction
    GPIO.output(DIG2, GPIO.LOW)         # set DIG2 as HIGH, to control direction
    p1.start(RUNSPEED)                        # set speed for M1 at 100%
    p2.start(RUNSPEED)                        # set speed for M2 at 100%
    #sleep(DELAY)                             #delay for 2 second
    return 0

## reverseLeft ########################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#
#
#######################################################
def reverseLeft():
    print("    Reverse-Left")
    GPIO.output(DIG1, GPIO.LOW)         # set DIG1 as HIGH, to control direction
    GPIO.output(DIG2, GPIO.LOW)         # set DIG2 as HIGH, to control direction
    p1.start(RUNSPEED - TURN)                        # set speed for M1 at 100%
    p2.start(RUNSPEED)                        # set speed for M2 at 100%
    #sleep(DELAY)                             #delay for 2 second
    return 0

## reverseRight #######################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#
#
#######################################################
def reverseRight():
    print("    Reverse-Right")
    GPIO.output(DIG1, GPIO.LOW)         # set DIG1 as HIGH, to control direction
    GPIO.output(DIG2, GPIO.LOW)         # set DIG2 as HIGH, to control direction
    p1.start(RUNSPEED)                        # set speed for M1 at 100%
    p2.start(RUNSPEED - TURN)                        # set speed for M2 at 100%
    #sleep(DELAY)                             #delay for 2 second
    return 0
