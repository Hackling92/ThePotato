#########################################################################################################################################################################################################################

# Imports Libraries to Run the rest of the program   
import pygame                                                           #pygame controller library
import time                                                             #Time library 
import RPi.GPIO as GPIO                                                 #Raspberry Pi GPIO pin library, initiates GPIO pins
import os                                                               #Imports the operating system library
from time import sleep                                                  #Import sleep functions from time library

# GPIO setups
GPIO.setmode(GPIO.BCM)                                                  # GPIO library setups
GPIO.setwarnings(False)

########################################################################################################################################################################################################################
#GPIO Pins For Motor Controller (PWM PIN and DIRECTION PIN), where the left motor is #1 and right motor is #2 
RightMP = 24                                                            #PWM2 PIN for Right Motor
LeftMP = 23                                                             #PWM1 PIN for Left Motor
RightMD = 8                                                             #DIR2 PIN for Right Motor
LeftMD = 7                                                              #DIR1 PIN for Left Motor

#GPIO Pins for the Front and side ultrasonic sensor pins for the Trigger and Echo output and inputs: The ultrasonic sensors uses the same input for both the Trigger and Echo
sensorSigFront1Trig = 6                                                 #Left Front Ultrasonic Sensor Trigger GPIO Pin
sensorSigFront1Echo = 6                                                 #Left Front Ultrasonic Sensor Echo GPIO Pin
sensorSigFront2Trig = 5                                                 #Right Front Ultrasonic Sensor Trigger GPIO Pin
sensorSigFront2Echo = 5                                                 #Right Front Ultrasonic Sensor Echo GPIO Pin
sensorSigSide1Trig = 19                                                 #Left Side Ultrasonic Sensor Trigger GPIO Pin
sensorSigSide1Echo = 19                                                 #Left Side Ultrasonic Sensor Echo GPIO Pin
sensorSigSide2Trig = 13                                                 #Right Side Ultrasonic Sensor Trigger GPIO Pin
sensorSigSide2Echo = 13                                                 #Right Side Ultrasonic Sensor Echo GPIO Pin

#GPIO Pin Output or Input 
GPIO.setup(RightMP,GPIO.OUT)                                            #Initiate PWM2 pin for Right Motor as an output
GPIO.setup(LeftMP,GPIO.OUT)                                             #Initiate PWM1 pin for Left Motor as an output
GPIO.setup(RightMD,GPIO.OUT)                                            #Initiate DIR2 pin for Right Motor as an output
GPIO.setup(LeftMD,GPIO.OUT)                                             #Initiate DIR1 pin for Left Motor as an output
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)                       #Initiate Emergency Stop Button as an input

#ULTRA
GPIO.setup(sensorSigFront1Trig, GPIO.IN)                                #Initiate Left Front Sensor Trigger GPIO Input
GPIO.setup(sensorSigFront2Trig, GPIO.IN)                                #Initiate Right Front Sensor Trigger GPIO Input
GPIO.setup(sensorSigSide1Trig, GPIO.IN)                                 #Initiate Left Side Sensor Trigger GPIO Input
GPIO.setup(sensorSigSide2Trig, GPIO.IN)                                 #Initiate Right Side Sensor Trigger GPIO Input

GPIO.setup(sensorSigFront1Echo, GPIO.OUT)                               #Initiate Left Front Sensor Echo GPIO Output
GPIO.setup(sensorSigFront2Echo, GPIO.OUT)                               #Initiate Right Front Sensor Echo GPIO Output
GPIO.setup(sensorSigSide1Echo, GPIO.OUT)                                #Initiate Left Side Sensor Echo GPIO Output
GPIO.setup(sensorSigSide2Echo, GPIO.OUT)                                #Initiate Right Side Sensor Echo GPIO Output


########################################################################################################################################################################################################################
#Variable definition for the left and right motor of the up and down motion with PWM variables, and starting PWM Values

# Variables
LeftMotorUD = 0                                                         # Initial value For left motor Up and Down Joystick value 
RightMotorUD = 0                                                        # Initial value For Right Motor Up and Down Joystick Value

# Setup PWM
p1 = GPIO.PWM(LeftMP,100)                                               #PWM variable for left motor PWM pin 
p2 = GPIO.PWM(RightMP,100)                                              #PWM variable for right motor PWM pin
p1.start(0)                                                             #Initial Value of the Left Motor PWM value at 0%
p2.start(0)                                                             #Initial Value of the Right Motor PWM value at 0%

#########################################################################################################################################################################################################################
#Initializes the GamePad (Logitech F310 Digital Input (D-Mode))   

# Initialize pygame
pygame.init()                                                           #Initialize pygame library

# Wait for a joystick
while pygame.joystick.get_count() == 0:                                                 #When the pygame library is looking for USB port 
        print "Waiting for joystick count = %i" % pygame.joystick.get_count()           #Prints waiting for joystick if the joystick has not been connected.
        time.sleep(10)                                                                  #waits 10 seconds until GamePad gets controller
        pygame.joystick.quit()                                                          #After 10 seconds the program ends search
        pygame.joystick.init()                                                          #Then reinitiates the pygame to look for the gamepad

j = pygame.joystick.Joystick(0)                                                         #Makes the joystick connected to the USB Port a variable
j.init()                                                                                #Initiates the joystick variable/ just the joystick

# % of joystick movement to use motors ex.(25 = 25%)
threshold = 10                                                                          #Need a Duty Cycle % of 10% to initiate  

##########################################################################################################################################################################################################################
# This section of the code is to indicate the Axis and Button numbers found from running " jstest /dev/input/js0 " in the pi terminal. Then pressing each button/axis to indicate which input was used. ON/OFF for buttons
                                                                                                                                                                              # -32767 forward and 32767 backward for axis

# Key mappings for pygame.JOYAXISMOTION
AXIS_LEFT_JOYSTICK_VERTICAL = 1                                                         #Pygame axis values for Left joystick in the vertical direction (-32767 up, 32767 down, 0 neutral)
AXIS_LEFT_JOYSTICK_HORIZONTAL = 0                                                       #Pygame axis values for Left joystick in the horizontal direction (-32767 left, 32767 right, 0 neutral)
AXIS_RIGHT_JOYSTICK_VERTICAL = 3                                                        #Pygame axis values for Right joystick in the vertical direction (-32767 up, 32767 down, 0 neutral)
AXIS_RIGHT_JOYSTICK_HORIZONTAL = 2                                                      #Pygame axis values for right joystick in the horizontal direction (-32767 left, 32767 right, 0 neutral)
DPAD_UP_DOWN = 5                                                                        #Pygame axis values for D-Pad in the vertical direction (-32767 up, 32767 down)
DPAD_LEFT_RIGHT = 4                                                                     #Pygame axis values for D-Pad in the horizontal direction (-32767 left, 32767 right)

#Key mapping for pygame.JOYBUTTONUP
LEFT_TRIGGER_LB = 4                                                                     #pygame button values for Bottom Left Trigger (ON/OFF)
LEFT_TRIGGER_LT = 6                                                                     #pygame button values for Top Left Trigger (ON/OFF)
RIGHT_TRIGGER_LB = 5                                                                    #pygame button values for Bottom Right Trigger (ON/OFF)
RIGHT_TRIGGER_LT = 7                                                                    #pygame button values for Top Right Trigger (ON/OFF)
X_BUTTON = 0                                                                            #pygame button values for X Button on F310 Controller (ON/OFF)
Y_BUTTON = 3                                                                            #pygame button values for Y Button on F310 Controller (ON/OFF)
A_BUTTON = 1                                                                            #pygame button values for A Button on F310 Controller (ON/OFF)
B_BUTTON = 2                                                                            #pygame button values for B Button on F310 Controller (ON/OFF)
BACK = 8                                                                                #pygame button values for Back Button on F310 Controller (ON/OFF)
START = 9                                                                               #pygame button values for Start Button on F310 Controller (ON/OFF)
LEFT_JOYSTICK_BUTTON = 10                                                               #pygame button values for Left Joystick Button on F310 Controller (ON/OFF)
RIGHT_JOYSTICK_BUTTON = 11                                                              #pygame button values for Right Joystick Button on F310 Controller (ON/OFF)

#############################################################################################################################################################################################################################
##This is a temperature measurement definition variable
def measure_temperature():
        temperature = os.popen("vcgencmd measure_temp").readline()                      #Retrieves temperature of the raspberry pi motherboard 
        return (temperature.replace("temp=",""))                                        


##This is for the Front two Ultrasonic sensors that are on the iRobot. This code converts the signals that the ultrasonic sensor is reading into a distance value in units of cm
def distance1():
        #Set Tigger to High
        GPIO.output(sensorSigFront1Trig, True)                                          #Set front ultrasonic sensor 1 trigger ON                                          
        GPIO.output(sensorSigFront2Trig, True)                                          #Set front ultrasonic sensor 2 trigger ON

        #Set Trigger after 0.02ms to Low
        time.sleep(0.00002)                                                             #Delay triggers for 2 microseconds
        GPIO.output(sensorSigFront1Echo, False)                                         #Set front ultrasonic sensor 1 trigger OFF
        GPIO.output(sensorSigFront2Echo, False)                                         #Set front ultrasonic sensor 2 trigger OFF

        StartTime1 = time.time()                                                        #Initial Start Time (In Seconds)
        StopTime1 = time.time()                                                         #Initial Stop Time (In Seconds)  

        #Save Start Time
        while GPIO.input(sensorSigFront1Trig) == 0 and GPIO.input(sensorSigFront2Trig) == 0:    #While the two front sensors echo are OFF
                StartTime1 = time.time()                                                        #Record time at OFF, start of pulse
                
        #Save time of Arrival
        while GPIO.input(sensorSigFront1Echo) == 1 and GPIO.input(sensorSigFront2Echo) == 1:    #While the two front sensors echo are ON
                StopTime1 = time.time()                                                         #Record time at ON, end of pulse
        #Time Difference Between start and arrival
        pulse_duration1 = StopTime1 - StartTime1                                                #Calculate the time taken from start to end of pulse from front sensors

        #Converts Time to Distance
        distance1 = pulse_duration1*17000                                                       #Calculate distance that pulse traveled, (time*(34000cm/s))/2
        distance1 = round(distance1, 2)                                                         #Round distance to 2 decimal places

        return distance1

##This is for the Left and Right Ultrasonic sensors that are on the iRobot. This code converts the signals that the ultrasonic sensor is reading into a distance value in units of cm
def distance2():                                                                

        #Set Tigger to High
        GPIO.output(sensorSigSide1Trig, True)                                           #Set front ultrasonic sensor 1 trigger ON
        GPIO.output(sensorSigSide2Trig, True)                                           #Set front ultrasonic sensor 2 trigger ON

        #Set Trigger after 0.02ms to Low
        time.sleep(0.00002)                                                             #Delay triggers for 2 microseconds
        GPIO.output(sensorSigSide1Echo, False)                                          #Set front ultrasonic sensor 1 trigger OFF
        GPIO.output(sensorSigSide2Echo, False)                                          #Set front ultrasonic sensor 2 trigger OFF

        StartTime2 = time.time()                                                        #Initial Start Time (In Seconds)
        StopTime2 = time.time()                                                         #Initial Stop Time (In Seconds)

        #Save Start Time
        while GPIO.input(sensorSigSide1Trig) == 0 and GPIO.input(sensorSigSide2Trig) == 0:      #While the two front sensors echo are OFF
                StartTime2 = time.time()                                                        #Record time at OFF, start of pulse
                
        #Save time of Arrival
        while GPIO.input(sensorSigSide1Echo) == 1 and GPIO.input(sensorSigSide2Echo) == 1:      #While the two front sensors echo are ON
                StopTime2 = time.time()                                                         #Record time at ON, end of pulse

        #Time Difference Between start and arrival
        pulse_duration2 = StopTime2 - StartTime2                                                #Calculate the time taken from start to end of pulse from front sensors

        #Converts Time to Distance
        distance2 = pulse_duration2*17000                                                       #Calculate distance that pulse traveled, (time*(34000cm/s))/2
        distance2 = round(distance2, 2)                                                         #Round distance to 2 decimal places

        return distance2

###########################################################################################################################################################################################################################  
try:
        while True:
                # Main Control System to run a differential motor controller with Left and Right joysticks on a Logitech F310 GamePad
                events = pygame.event.get()                                     #Grabs the events file in the pygame library 
                input_state = GPIO.input(16)                                    #Input GPIO input for the emergency stop buttons on the body of the iRobot
                print(measure_temperature())                                    #Prints out motherboard temperature
###########################################################################################################################################################################################################################
## This part of the code is meant to put in the distances that are being calculated in distance1 and distance2 definition functions into the controller code. 
##                dist1 = distance1()
##                dist2 = distance2()
##                print ("Measured Distance1 = %.1f cm" % dist1)
##                print ("Measured Distance2 = %.1f cm" % dist2)
###########################################################################################################################################################################################################################
##This part of the code is to use the emergency stop buttons that are physically on the iRobot hood. You can push any button to initiate the emergency stop
                
                if input_state == True:                                       #If the button is pressed(true) then do the rest 
                        print('Emergency Stop')                               #Print Emergency Stop
                        p1.ChangeDutyCycle(0)                                 #PWM duty cycle equals 0.00% for Left motor
                        p2.ChangeDutyCycle(0)                                 #PWM duty cycle equals 0.00% for Right motor
                        time.sleep(10)                                        #Wait 10 seconds before the Joy-Stick can be re-engaged
                        print('Joy-Stick Re-Engaged')                         #Print Joy stick re-engaged                       
###########################################################################################################################################################################################################################

                for event in events:
                        UpdateMotorsL = 0                                     #Initial motor event for the Left Motor, saying the motor is not running
                        UpdateMotorsR = 0                                     #Initial motor event for the Right Motor, saying the motor is not running

                        if event.type == pygame.JOYBUTTONUP:                    #Left Trigger Top: Using this button to shut down the raspberry pi safely 
                                if event.button == 6:                           #When pressing bottom left trigger
                                        time.sleep(3)                           #wait 3 seconds 
                                        print "Shutting Down Pi"                #Then print Shutting Down Pi
                                        time.sleep(3)                           #Wait 3 seconds again
                                        os.system("sudo shutdown -h now")       #Safely Shut Down Raspberry Pi
                                        
                                        
                                if event.button == 7:                           #Right Trigger LT button: Using this button to restart the raspberry pi
                                        time.sleep(3)                           #Wait 3 seconds                           
                                        print "Restarting Pi/Program"           #Then Print restarting pi/program
                                        time.sleep(3)                           #Wait 3 seconds again
                                        os.system("sudo reboot")                #Reboot the Raspberry Pi safely 
                                                
                                        
                                if event.button == 2:                           #B Button: This is going to act as a 2nd emergency stop button for the GamePad
                                        print('Emergency Stop (JoyStick)')      #Print Emergency Stop (JoyStick)
                                        p1.ChangeDutyCycle(0)                   #PWM duty cycle equals 0.00% for motor 1
                                        p2.ChangeDutyCycle(0)                   #PWM duty cycle equals 0.00% for motor 2
                                        time.sleep(10)                          #Wait 10 seconds before the Joy-Stick can be re-engaged
                                        print('Joy-Stick Re-Engaged')           #Print Joy stick re-engaged
                                        
                                        
                        if event.type == pygame.JOYAXISMOTION:
                                if event.axis == 1:                           #Left Motor axis port from pygame
                                        LeftMotorUD = 100*(event.value)       #Reads the values from the left joystick in duty cycle values  
                                        UpdateMotorsL = 1                     #Updates left motor to say that the motor has been turned on
                                        #print "Left Motor %i" % LeftMotorUD   #Shows the value of the Duty cycle % and the direction with  (-100% being Forward, 100% being backward)
                                        
                                elif event.axis == 3:                         #Right Motor axis port from pygame 
                                        RightMotorUD = 100*(event.value)      #Reads the values from the right joystick in duty cycle values 
                                        UpdateMotorsR = 1                     #Updates right motor to say that the motor has been turned on
                                        #print "Right %i" % RightMotorUD       #Shows the value of the Duty cycle % and the direction with  (-100% being Forward, 100% being backward)      




                                # Motor update: This translates the Left joystick duty cycle value to translate motor speed
                                if UpdateMotorsL:      
                                        if (-101 <= LeftMotorUD <= -threshold): # Left Motor Forward
                                                GPIO.output(LeftMD,1)           #Changes direction forward
                                                speed = -1*int(LeftMotorUD)     #Equation that converts the output of the joystick to speed duty cycle percent (%)
                                                if speed >= 74:                 #This logic is to limit the duty cycle% to 73.0% max. This equates to the speed of 3.56 km/hr 
                                                        speed=73
                                                else:
                                                        speed = speed

                                                p1.ChangeDutyCycle(speed)       #Changes PWM value
                                                
##########################################################################################################################################################################################
## This logic was to limit the duty cycle % for the speed of the left motor forward. Was not able to integrate the ultrasonic sensors with the code because the sensors does not function consistantly. 
##                                                if dist1 >= 15 and dist1 <= 63:
##                                                        speed = 25
##
##                                                elif dist1 >= 64 and dist1 <= 183:
##                                                        speed = 50
##                                                else:
##                                                        speed = speed
###########################################################################################################################################################################################                                                

                                                

                                        elif (100 >= LeftMotorUD >= threshold): # Left Motor Backward
                                                GPIO.output(LeftMD,0)           #Changes direction Backward
                                                speed = int(LeftMotorUD)        #Equation that converts the output of the joystick to speed duty cycle percent (%)
                                                if speed >= 74:                 #This logic is to limit the duty cycle% to 73.0% max. This equates to the speed of 3.56 km/hr
                                                        speed=73
                                                else:
                                                        speed = speed

                                                p1.ChangeDutyCycle(speed)       #Changes PWM value 

#######################################################################################################################################################################
##This logic was to limit the duty cycle % for the speed of the left motor backward. Was not able to integrate the ultrasonic sensors with the code because the sensors does not function consistantly.
##                                                if dist1 >= 15 and dist1 <= 63:
##                                                        speed = 25
##
##                                                elif dist1 >= 64 and dist1 <= 183:
##                                                        speed = 50
##                                                else:
##                                                        speed = speed
#######################################################################################################################################################################                                                

                                               

                                        else: 
                                                GPIO.output(LeftMD,0)           #Turns off left Motor
                                                p1.ChangeDutyCycle(0)           #Changes the Duty cycle % to 0%

                                if UpdateMotorsR:
                                        if (-101 <= RightMotorUD <= -threshold): # Right Motor Forward
                                                GPIO.output(RightMD,1)          #Changes direction forward
                                                speed = -1*int(RightMotorUD)    #Equation that converts the output of the joystick to speed duty cycle percent (%)
                                                if speed >= 74:                 #This logic is to limit the duty cycle% to 73.0% max. This equates to the speed of 3.56 km/hr
                                                        speed=73
                                                else:
                                                        speed = speed

                                                p2.ChangeDutyCycle(speed)       #Changes PWM value

#######################################################################################################################################################################
##This logic was to limit the duty cycle % for the speed of the Right motor Forward. Was not able to integrate the ultrasonic sensors with the code because the sensors does not function consistantly.
##                                                if dist1 >= 15 and dist1 <= 63:
##                                                        speed = 25
##
##                                                elif dist1 >= 64 and dist1 <= 183:
##                                                        speed = 50
##                                                else:
##                                                        speed = speed     
#######################################################################################################################################################################

                                                

                                        elif (100 >= RightMotorUD >= threshold): #Right Motor Backwards
                                                GPIO.output(RightMD,0)          #Changes direction Backward
                                                speed = int(RightMotorUD)       #Equation that converts the output of the joystick to speed duty cycle percent (%)
                                                if speed >= 74:                 #This logic is to limit the duty cycle% to 73.0% max. This equates to the speed of 3.56 km/hr
                                                        speed=73
                                                else:
                                                        speed = speed

                                                p2.ChangeDutyCycle(speed)       #Changes PWM value

#######################################################################################################################################################################
##This logic was to limit the duty cycle % for the speed of the Right motor backwards. Was not able to integrate the ultrasonic sensors with the code because the sensors does not function consistantly.
##                                                if dist1 >= 15 and dist1 <= 63:
##                                                        speed = 25
##
##                                                elif dist1 >= 64 and dist1 <= 183:
##                                                        speed = 50
##                                                else:
##                                                        speed = speed
#######################################################################################################################################################################
                                                        
                                               
                                                
                                        else: 
                                                GPIO.output(RightMD,0)          #Turns off right Motor
                                                p2.ChangeDutyCycle(0)           #Changes the Duty cycle % to 0%

                                
except KeyboardInterrupt:                                                       #Ends While loop
        j.quit()                                                                #Ends GamePad from working
        p1.stop(0)                                                              #PWM duty cycle equals 0.00% for motor 1
        p2.stop(0)                                                              #PWM duty cycle equals 0.00% for motor 2
        GPIO.cleanup()                                                          #Cleans up GPIO ports to prevent damage to the raspberry Pi

print("Working Things Out :( ") 
