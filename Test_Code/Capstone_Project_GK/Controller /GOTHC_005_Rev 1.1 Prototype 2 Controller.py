from evdev import InputDevice, categorize, ecodes, KeyEvent

gamepad = InputDevice('/dev/input/event0')

#Button Code
LBTrig = 292
LTTrig = 294
RBTrig = 293
RTTrig = 295

Xbutton= 288
Ybutton= 291
Abutton= 289
Bbutton= 290

LJoyC = 298
RJoyC = 299

Back= 296
start= 297

#Axis
LeftJoy=
RightJoy=RZ


import pygame
import RPi.GPIO as GPIO                 # using Rpi.GPIO module
from time import sleep                  # import function sleep for delay
GPIO.setmode(GPIO.BCM)                  # GPIO numbering
GPIO.setwarnings(False)                 # enable warning from GPIO
AN2 = 24                                # set pwm2 pin on MD10-Hat
AN1 = 23                                # set pwm1 pin on MD10-hat
DIG2 = 8                                # set dir2 pin on MD10-Hat
DIG1 = 7                                # set dir1 pin on MD10-Hat
GPIO.setup(AN2, GPIO.OUT)               # set pin as output
GPIO.setup(AN1, GPIO.OUT)               # set pin as output
GPIO.setup(DIG2, GPIO.OUT)              # set pin as output
GPIO.setup(DIG1, GPIO.OUT)              # set pin as output
sleep(1)                                # delay for 1 seconds
p1 = GPIO.PWM(AN1, 100)                 # set pwm for M1
p2 = GPIO.PWM(AN2, 100)                 # set pwm for M2

def motorForward(DIG1):
   print "Forward"
   GPIO.output(DIG1, GPIO.LOW)          # set DIG1 as LOW, to control direction
  #GPIO.output(DIG2, GPIO.LOW)          # set DIG2 as LOW, to control direction
   p1.start(50)                        # set speed for M1 at 100%   
  #p2.start(100)                        # set speed for M2 at 100%
   sleep(2)                             #delay for 2 second

def motorStop():
   print "Stop"
   GPIO.output(DIG1, GPIO.LOW)          # Direction can ignore
  #GPIO.output(DIG2, GPIO.LOW)          # Direction can ignore
   p1.start(0)                          # set speed for M1 at 0%
  #p2.start(0)                          # set speed for M2 at 0%
   sleep(3)                             #delay for 3 second

def motorBackward(DIG1):
   print "Backward"
   GPIO.output(DIG1, GPIO.HIGH)         # set DIG1 as HIGH, to control direction
  #GPIO.output(DIG2, GPIO.HIGH)         # set DIG2 as HIGH, to control direction
   p1.start(50)                        # set speed for M1 at 100%
  #p2.start(100)                        # set speed for M2 at 100%
   sleep(2)                             #delay for 2 second

def main():

        for event in gamepad.read_loop():
                if event.type == ecodes.EV_KEY and event.type == ecodes.EV_ABS and event.type == 1: 
                        if event.code == LeftJoy: # keyevent.keycode =='BTN_JOYSTICK':
                                print "Left Motor Forward"
                                motorForward(DIG1)
                        elif event.code == LeftJoy: #keyevent.keycode == 'BTN_TOP':
                                print "Left Motor Backward"
                                motorBackward(DIG1)
                        elif event.code == RightJoy: #keyevent.keycode == 'BTN_THUMB':
                                print "Right Motor Forward"
                                motorForward(DIG2)
                        elif event.code == RightJoy: #keyevent.keycode == 'BTN_THUMB2':
                                print "Right Motor Backward"
                                motorBackward(DIG2)
                        elif event.code == LTrig: #keyevent.keycode == 'BTN_PINKIE':
                                print "Stop iRobot"
                                motorStop()                                                   
			
main()
