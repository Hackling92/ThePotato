# Import Files From Pi 
import pygame                                                         #pygame controller library
import time                                                           #Time library 
import RPi.GPIO as GPIO                                               #Raspberry Pi GPIO pin library, initiates GPIO pins
import os



# GPIO setups
GPIO.setmode(GPIO.BCM)                                                # GPIO library setups
GPIO.setwarnings(False)


RightMP = 24                                                          #PWM2 PIN on MD10-Hat for Right Motor
LeftMP = 23                                                           #PWM1 PIN on MD10-Hat for Left Motor
RightMD = 8                                                           #DIR2 PIN on MD10-Hat for Right Motor
LeftMD = 7                                                            #DIR1 PIN on MD10-Hat for Left Motor

GPIO.setup(RightMP,GPIO.OUT)                                          #Initiate PWM2 pin for Right Motor
GPIO.setup(LeftMP,GPIO.OUT)                                           #Initiate PWM1 pin for Left Motor
GPIO.setup(RightMD,GPIO.OUT)                                          #Initiate DIR2 pin for Right Motor
GPIO.setup(LeftMD,GPIO.OUT)                                           #Initiate DIR1 pin for Left Motor
#GPIO.setup(20,GPIO.OUT) # Red LED
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Variables
LeftMotorUD = 0                                                       # Initial value For left motor Up and Down Joystick value 
RightMotorUD = 0                                                      # Initial value For Right Motor Up and Down Joystick Value

# Setup PWM
p1 = GPIO.PWM(LeftMP,100)                                             #PWM variable for left motor PWM pin 
p2 = GPIO.PWM(RightMP,100)                                            #PWM variable for right motor PWM pin


p1.start(0)                                                           #Initial Value of the Left Motor PWM value at 0%
p2.start(0)                                                           #Initial Value of the Right Motor PWM value at 0%


# Initialize pygame
pygame.init()                                                         #Initialize pygame library

# Wait for a joystick
while pygame.joystick.get_count() == 0:                               #When the pygame library is looking for USB port 
        print "Waiting for joystick count = %i" % pygame.joystick.get_count() #Prints waiting for joystick if the joystick has not been connected.
        time.sleep(10)                                                        #waits 10 seconds until GamePad gets controller
        pygame.joystick.quit()                                                #After 10 seconds the program ends search
        pygame.joystick.init()                                                #Then reinitiates the pygame to look for the gamepad

j = pygame.joystick.Joystick(0)                                               #Makes the joystick connected to the USB Port a variable
j.init()                                                                      #Initiates the joystick variable/ just the joystick

# % of joystick movement to use motors ex.(25 = 25%)
threshold = 10                                                                #Need a Duty Cycle % of 10 to initiate  


# Key mappings for pygame.JOYAXISMOTION
AXIS_LEFT_JOYSTICK_VERTICAL = 1                                                        #Pygame axis values for Left joystick in the vertical direction
AXIS_LEFT_JOYSTICK_HORIZONTAL = 0
AXIS_RIGHT_JOYSTICK_VERTICAL = 3                                                       #Pygame axis values for Right joystick in the vertical direction
AXIS_RIGHT_JOYSTICK_HORIZONTAL = 2
DPAD_UP_DOWN = 5
DPAD_LEFT_RIGHT = 4

#Key mapping for pygame.KEYUP
LEFT_TRIGGER_LB = 4
LEFT_TRIGGER_LT = 6
RIGHT_TRIGGER_LB = 5
RIGHT_TRIGGER_LT = 7
X_BUTTON = 0
Y_BUTTON = 3
A_BUTTON = 1
B_BUTTON = 2
BACK = 8
START = 9
LEFT_JOYSTICK_BUTTON = 10
RIGHT_JOYSTICK_BUTTON = 11


try:
        while True:
                # Main Control System to run a differential motor controller with Left and Right joysticks on a Logitech F310 GamePad
                events = pygame.event.get()
                input_state = GPIO.input(16)
                time.sleep(5) 

##                if input_state == True:
##                        print('Emergency Program Stop')
##                        j.quit()
##                        p1.stop(0)
##                        p2.stop(0)
##                        GPIO.cleanup()


                for event in events:
                        UpdateMotorsL = 0                                     #Initial motor event for the Left Motor, saying the motor is not running
                        UpdateMotorsR = 0                                     #Initial motor event for the Right Motor, saying the motor is not running

                        if event.type == pygame.JOYBUTTONUP:
                                if event.button == 6:
                                        shut_down_button = time.time()
                                        os.system("sudo shutdown -h now")
                                        print "This works"
                                if event.button == 7:                         #Right Trigger LT button: Using this button to restart the raspberry pi
                                        restart_down_button = time.time()
                                        os.system("sudo reboot")
                                        print "Restarted Baby"

                        if event.type == pygame.JOYAXISMOTION:
                                if event.axis == 1:                           #Left Motor axis port from pygame
                                        LeftMotorUD = 100*(event.value)       #Reads the values from the left joystick in duty cycle values  
                                        UpdateMotorsL = 1                     #Updates left motor to say that the motor has been turned on
                                        print "Left Motor %i" % LeftMotorUD   #Shows the value of the Duty cycle % and the direction with  (-100% being Forward, 100% being backward)
                                        
                                elif event.axis == 3:                         #Right Motor axis port from pygame 
                                        RightMotorUD = 100*(event.value)      #Reads the values from the right joystick in duty cycle values 
                                        UpdateMotorsR = 1                     #Updates right motor to say that the motor has been turned on
                                        print "Right %i" % RightMotorUD       #Shows the value of the Duty cycle % and the direction with  (-100% being Forward, 100% being backward)      

                                # Motor update: This translates the Left joystick duty cycle value to translate motor speed
                                if UpdateMotorsL:      
                                        if (-101 <= LeftMotorUD <= -threshold): # Left Motor Forward
                                                GPIO.output(LeftMD,1)           #Changes direction forward
                                                speed = -1*int(LeftMotorUD)
                                                p1.ChangeDutyCycle(speed)       #Changes PWM value 

                                        elif (100 >= LeftMotorUD >= threshold): # Left Motor Backward
                                                GPIO.output(LeftMD,0)           #Changes direction Backward
                                                speed = int(LeftMotorUD)
                                                p1.ChangeDutyCycle(speed)       #Changes PWM value 

                                        else: 
                                                GPIO.output(LeftMD,0)           #Turns off Motor
                                                p1.ChangeDutyCycle(0)

                                if UpdateMotorsR:
                                        if (-101 <= RightMotorUD <= -threshold): # Right Motor Forward
                                                GPIO.output(RightMD,1)          #Changes direction forward
                                                speed = -1*int(RightMotorUD)
                                                p2.ChangeDutyCycle(speed)       #Changes PWM value

                                        elif (100 >= RightMotorUD >= threshold): #Right Motor Backwards
                                                GPIO.output(RightMD,0)          #Changes direction Backward
                                                speed = int(RightMotorUD) 
                                                p2.ChangeDutyCycle(speed)       #Changes PWM value
                                                
                                        else: 
                                                GPIO.output(RightMD,0)          #Turns off Motor
                                                p2.ChangeDutyCycle(0)
                                
                                        
