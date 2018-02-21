#This code was taken from the website: https://www.robotshop.com/en/cytron-13a-5-30v-single-dc-motor-controller.html#description
#This code was provided for the motorcontrollers used for cytron 13A, 5-30V motor controller


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

try:
  while True:
   
   print "Forward"
   GPIO.output(DIG1, GPIO.LOW)          # set DIG1 as LOW, to control direction
  #GPIO.output(DIG2, GPIO.LOW)          # set DIG2 as LOW, to control direction
   p1.start(15)                        # set speed for M1 at 100%   
  #p2.start(100)                        # set speed for M2 at 100%
   sleep(2)                             #delay for 2 second

   print "STOP"
   GPIO.output(DIG1, GPIO.LOW)          # Direction can ignore
  #GPIO.output(DIG2, GPIO.LOW)          # Direction can ignore
   p1.start(0)                          # set speed for M1 at 0%
  #p2.start(0)                          # set speed for M2 at 0%
   sleep(3)                             #delay for 3 second

   print "Backward"
   GPIO.output(DIG1, GPIO.HIGH)         # set DIG1 as HIGH, to control direction
  #GPIO.output(DIG2, GPIO.HIGH)         # set DIG2 as HIGH, to control direction
   p1.start(15)                        # set speed for M1 at 100%
  #p2.start(100)                        # set speed for M2 at 100%
   sleep(2)                             #delay for 2 second

   print "STOP"
   GPIO.output(DIG1, GPIO.LOW)          # Direction can ignore
  #GPIO.output(DIG2, GPIO.LOW)          # Direction can ignore
   p1.start(0)                          # set speed for M1 at 0%
  #p2.start(0)                          # set speed for M2 at 0%
   sleep(3)                             #delay for 3 second


except:                                 # exit programe when keyboard interupt
   p1.start(0)                          # set speed to 0
  #p2.start(0)                          # set speed to 0
                                        # Control+x to save file and exit
