# Import Files From Pi 
import pygame                   #pygame controller library
import time                     #Time library 
import RPi.GPIO as GPIO         #Raspberry Pi 



# GPIO setups
GPIO.setmode(GPIO.BCM)          # GPIO library setups
GPIO.setwarnings(False)


RightMP = 24                    #PWM2 PIN on MD10-Hat for Right Motor
LeftMP = 23                     #PWM1 PIN on MD10-Hat for Left Motor
RightMD = 8                     #DIR2 PIN on MD10-Hat for Right Motor
LeftMD = 7                      #DIR1 PIN on MD10-Hat for Left Motor

GPIO.setup(RightMP,GPIO.OUT)    #Initiate PWM2 pin for Right Motor
GPIO.setup(LeftMP,GPIO.OUT)     #Initiate PWM1 pin for Left Motor
GPIO.setup(RightMD,GPIO.OUT)    #Initiate DIR2 pin for Right Motor
GPIO.setup(LeftMD,GPIO.OUT)     #Initiate DIR1 pin for Left Motor
#GPIO.setup(20,GPIO.OUT) # Red LED

# Variables
LeftMotorUD = 0                 # Initial value For left motor Up and Down Joystick value 
RightMotorUD = 0                # Initial value For Right Motor Up and Down Joystick Value

# Setup PWM
p1 = GPIO.PWM(LeftMP,100)       #PWM variable 
p2 = GPIO.PWM(RightMP,100)


p1.start(0)
p2.start(0)


# Initialize pygame
pygame.init()

# Wait for a joystick
while pygame.joystick.get_count() == 0:
        print "Waiting for joystick count = %i" % pygame.joystick.get_count()
        time.sleep(10)
        pygame.joystick.quit()
        pygame.joystick.init()

j = pygame.joystick.Joystick(0)
j.init()

# Needs ...% of joystick movement to use motors (0.25 = 25%)
threshold = 10


# Key mappings
AXIS_LEFT_VERTICAL = 1 
AXIS_RIGHT_VERTICAL = 3

try:
        while True:
                # Check for any queued events and then process each one
                events = pygame.event.get()
                for event in events:
                        UpdateMotorsL = 0
                        UpdateMotorsR = 0

                        # Check if one of the joysticks has moved
                        if event.type == pygame.JOYAXISMOTION:
                                if event.axis == 1: #Left Motor
                                        LeftMotorUD = 100*(event.value)
                                        UpdateMotorsL = 1
                                        print "Left Motor %i" % LeftMotorUD
                                        
                                elif event.axis == 3: #Right Motor 
                                        RightMotorUD = 100*(event.value)
                                        UpdateMotorsR = 1
                                        print "Right %i" % RightMotorUD      

                                # Motor update?
                                if UpdateMotorsL:      
                                        if (-101 <= LeftMotorUD <= -threshold): # Left Motor Forward
                                                GPIO.output(LeftMD,1)
                                                speed = -1*int(LeftMotorUD)
                                                p1.ChangeDutyCycle(speed)

                                        elif (100 >= LeftMotorUD >= threshold): # Left Motor Backward
                                                GPIO.output(LeftMD,0)
                                                speed = int(LeftMotorUD)
                                                p1.ChangeDutyCycle(speed)

                                        else: # Motors off
                                                GPIO.output(LeftMD,0)
                                                p1.ChangeDutyCycle(0)

                                if UpdateMotorsR:
                                        if (-101 <= RightMotorUD <= -threshold): # Right Motor Forward
                                                GPIO.output(RightMD,1)
                                                speed = -1*int(RightMotorUD)
                                                p2.ChangeDutyCycle(speed)

                                        elif (100 >= RightMotorUD >= threshold): # Right Motor Backwards
                                                GPIO.output(RightMD,0)
                                                speed = int(RightMotorUD) 
                                                p2.ChangeDutyCycle(speed)
                                                
                                        else: # Motors off
                                                GPIO.output(RightMD,0)
                                                p2.ChangeDutyCycle(0)

                                
except KeyboardInterrupt:
        j.quit()
        p1.stop(0)
        p2.stop(0)
        p3.stop(0)
        p4.stop(0)
        GPIO.cleanup()

print("Done")
