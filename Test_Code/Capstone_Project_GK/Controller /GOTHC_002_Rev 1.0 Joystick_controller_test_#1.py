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

#Axis Controller


#Library's needed to run the the program
import pygame
import RPi.GPIO as GPIO                 # using Rpi.GPIO module
from time import sleep                  # import function sleep for delay
GPIO.setmode(GPIO.BCM)                  # GPIO numbering
GPIO.setwarnings(False)                 # enable warning from GPIO

#Set PWM and DIR pins for Motor 1 and Motor 2
AN2 = 24                                # set pwm2 pin on MD10-Hat
AN1 = 23                                # set pwm1 pin on MD10-hat
DIG2 = 8                                # set dir2 pin on MD10-Hat
DIG1 = 7                                # set dir1 pin on MD10-Hat


LeftForBac = 0
RightForBac = 0
#Set the Drive pins as output pins
GPIO.setup(AN2, GPIO.OUT)               # set pin as output
GPIO.setup(AN1, GPIO.OUT)               # set pin as output
GPIO.setup(DIG2, GPIO.OUT)              # set pin as output
GPIO.setup(DIG1, GPIO.OUT)              # set pin as output
sleep(1)                                # delay for 1 seconds
p1 = GPIO.PWM(AN1, 100)                 # set pwm for M1
p2 = GPIO.PWM(AN2, 100)                 # set pwm for M2



def motorForward1(DIG1):
   print "Forward Motor 1"
   GPIO.output(DIG1, GPIO.LOW)          # set DIG1 as LOW, to control direction 
   p1.start(100)                        # set speed for M1 at 100% 
   sleep(0.01)
def motorForward2(DIG2):
   print "Forward Motor 2"
   GPIO.output(DIG2, GPIO.LOW)          # set DIG2 as LOW, to control direction
   p2.start(100)                        # set speed for M2 at 100%
   sleep(0.01)

def motorBackward1(DIG1):
   print "Backward Motor 1"
   GPIO.output(DIG1, GPIO.HIGH)         # set DIG1 as HIGH, to control direction
   p1.start(100)                        # set speed for M1 at 100%
   sleep(0.01)

def motorBackward2(DIG2):
   print "Backward Motor 2"
   GPIO.output(DIG2, GPIO.HIGH)          # set DIG2 as LOW, to control direction
   p2.start(100)                        # set speed for M2 at 100%
   sleep(0.01)

   
def motorStop1(DIG1):
   print "Stop Motor 1"
   GPIO.output(DIG1, GPIO.LOW)          # Direction can ignore
   p1.start(0)                          # set speed for M1 at 0%
                                  

def motorStop2(DIG2):
   print "Stop Motor 2"
   GPIO.output(DIG2, GPIO.LOW)          # Direction can ignore
   p2.start(0)                          # set speed for M2 at 0%
                                    
def main():

        for event in gamepad.read_loop():
                if event.type == ecodes.EV_KEY and event.type == 1 and event.type == pygame.JOYAXISMOTION: 
                        if event.axis == 1: # keyevent.keycode =='BTN_JOYSTICK':
                                print "Left Motor Forward"
                                LeftForBac = event.value
                                UpdateMotors = 1
   
                                motorForward1(DIG1)
                        elif event.code == Ybutton: #keyevent.keycode == 'BTN_TOP':
                                print "Left Motor Backward"
                                motorBackward1(DIG1)
                        elif event.axis == 3: #keyevent.keycode == 'BTN_THUMB':
                                print "Right Motor Forward"
                                motorForward2(DIG2)
                        elif event.code == Bbutton: #keyevent.keycode == 'BTN_THUMB2':
                                print "Right Motor Backward"
                                motorBackward2(DIG2)
                        elif event.code == LTTrig: #keyevent.keycode == 'BTN_PINKIE':
                                print "Stop Left motor"
                                motorStop1(DIG1)
                        elif event.code == RTTrig:
                                print "Stop Right Motor"
                                motorStop2(DIG2)
			
main()
