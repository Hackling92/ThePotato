from evdev import InputDevice, categorize, ecodes, KeyEvent
##def find_controller():
##
##      event0= InputDevice('/dev/input/event0')
##
##      event1= InputDevice('/dev/input/event1')
##
##      event2= InputDevice('/dev/input/event2')
##
##      event3= InputDevice('/dev/input/event3')
##
##      controller_list=["Logitech Gamepad F310"]
##
##      for controller in controller_list:
##         if event0.name == controller:
##            gamepad= event0
##            
##         elif event1.name == controller:
##            gamepad= event1
##            
##         elif event2.name == controller:
##            gamepad= event2
##            
##         elif event3.name == controller:
##            gamepad= event3
##            
##         else:
##               print("Controller not Found")
##      return gamepad
##gamepad = find_controller()

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
                if event.type == ecodes.EV_KEY and event.type == 1: 
                        if event.code == Xbutton: # keyevent.keycode =='BTN_JOYSTICK':
                                print "Left Motor Forward"
                                motorForward1(DIG1)
                        elif event.code == Ybutton: #keyevent.keycode == 'BTN_TOP':
                                print "Left Motor Backward"
                                motorBackward1(DIG1)
                        elif event.code == Abutton: #keyevent.keycode == 'BTN_THUMB':
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
