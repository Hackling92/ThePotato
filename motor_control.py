# PREVIOUS VERSIONS #
# This code was taken from the website: https://www.robotshop.com/en/cytron-13a-5-30v-single-dc-motor-controller.html#description
# This code was provided for the motorcontrollers used for cytron 13A, 5-30V motor controller

# CURRENT VERSION #
# This code was modified from the code used by the iRobot team of Fall 2017
# The primary modifications done by the CCP2 team was to implement the following...
#  - Skid Steer Command
#  - Various other control functions used for testing

#import pygame
import RPi.GPIO as GPIO                 # using Rpi.GPIO module
from time import sleep                  # import function sleep for delay
GPIO.setmode(GPIO.BOARD)                # GPIO numbering
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
TRACK_DISTANCE = 5

GPIO.setup(AN2, GPIO.OUT)               # set pin as output
GPIO.setup(AN1, GPIO.OUT)               # set pin as output
GPIO.setup(DIG2, GPIO.OUT)              # set pin as output
GPIO.setup(DIG1, GPIO.OUT)              # set pin as output
sleep(1)                                # delay for 1 seconds
p1 = GPIO.PWM(AN1, 100)                 # set pwm for M1
p2 = GPIO.PWM(AN2, 100)                 # set pwm for M2


# steer by setting one motor to zero and the other to the 50ish

## skidSteer ##########################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Skid steer algorithm that allows the
#               iRobot vehicle to make minute adjustments
#               to steering.
#######################################################
def skidSteer(dir, radius, speed, bearing):
    speedOuter = speed * ((radius+TRACK_DISTANCE)/radius)
    # Forward
    if(dir.lower() == "forward"):
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.HIGH)
        speedOuter = speed * ((radius+TRACK_DISTANCE)/radius)
        # Right or straight
        if(int(bearing) >= 0):
            p1.start(speed) # right side
            p2.start(speedOuter) # left  side
        # Left
        else:
            p1.start(speedOuter) # right side
            p2.start(speed) # left  side
    # Backward
    else:
        GPIO.output(DIG1, GPIO.HIGH)
        GPIO.output(DIG2, GPIO.LOW)
        # Right or straight
        if(int(bearing) >= 0):
            p1.start(speedOuter) # right side
            p2.start(speed) # left  side
        # Left
        else:
            p1.start(speed) # right side
            p2.start(speedOuter) # left  side

## fullStop ###########################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simple command to stop all movement
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
# Description:  Simple movement command used for vehicle
#               test purposes.
#
#######################################################
def forward(runspeed):
    print("    Forward")
    GPIO.output(DIG1, GPIO.HIGH)         # set DIG1 as LOW, to control direction
    GPIO.output(DIG2, GPIO.HIGH)         # set DIG2 as LOW, to control direction
    p1.start(runspeed)                   # set speed for M1 at 100%
    p2.start(runspeed)
    #sleep(DELAY)                        # delay for 2 second
    return 0

## forwardLeft ########################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simple movement command used for vehicle
#               test purposes.
#
#######################################################
def forwardLeft(runspeed):
    print("    Forward-Left")
    GPIO.output(DIG1, GPIO.HIGH)         # set DIG1 as LOW, to control direction
    GPIO.output(DIG2, GPIO.HIGH)         # set DIG2 as LOW, to control direction
    p1.start(runspeed)                   # set speed for M1 at 100%
    p2.start(runspeed - TURN)
    #sleep(DELAY)                        # delay for 2 second
    return 0

## forwardRight #######################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simple movement command used for vehicle
#               test purposes.
#
#######################################################
def forwardRight(runspeed):
    print("    Forward-Right")
    GPIO.output(DIG1, GPIO.HIGH)         # set DIG1 as LOW, to control direction
    GPIO.output(DIG2, GPIO.HIGH)         # set DIG2 as LOW, to control direction
    p1.start(runspeed - TURN)            # set speed for M1 at 100%
    p2.start(runspeed)
    #sleep(DELAY)                        # delay for 2 second
    return 0

## reverse ############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simple movement command used for vehicle
#               test purposes.
#
#######################################################
def reverse(runspeed):
    print("    Reverse")
    GPIO.output(DIG1, GPIO.LOW)          # set DIG1 as HIGH, to control direction
    GPIO.output(DIG2, GPIO.LOW)          # set DIG2 as HIGH, to control direction
    p1.start(runspeed)                   # set speed for M1 at 100%
    p2.start(runspeed)                   # set speed for M2 at 100%
    #sleep(DELAY)                        # delay for 2 second
    return 0

## reverseLeft ########################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simple movement command used for vehicle
#               test purposes.
#
#######################################################
def reverseLeft(runspeed):
    print("    Reverse-Left")
    GPIO.output(DIG1, GPIO.LOW)          # set DIG1 as HIGH, to control direction
    GPIO.output(DIG2, GPIO.LOW)          # set DIG2 as HIGH, to control direction
    p1.start(runspeed - TURN)            # set speed for M1 at 100%
    p2.start(runspeed)                   # set speed for M2 at 100%
    #sleep(DELAY)                        # delay for 2 second
    return 0

## reverseRight #######################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simple movement command used for vehicle
#               test purposes.
#
#######################################################
def reverseRight(runspeed):
    print("    Reverse-Right")
    GPIO.output(DIG1, GPIO.LOW)          # set DIG1 as HIGH, to control direction
    GPIO.output(DIG2, GPIO.LOW)          # set DIG2 as HIGH, to control direction
    p1.start(runspeed)                   # set speed for M1 at 100%
    p2.start(runspeed - TURN)            # set speed for M2 at 100%
    #sleep(DELAY)                        # delay for 2 second
    return 0

