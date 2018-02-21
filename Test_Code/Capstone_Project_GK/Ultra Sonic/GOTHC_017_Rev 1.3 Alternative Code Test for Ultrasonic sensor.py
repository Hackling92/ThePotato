import RPi.GPIO as GPIO      #Raspberry PI GPIO pin library initialization
import time                  #Time library
from time import sleep       #Import sleep functions from time library


GPIO.setmode(GPIO.BCM)       #GPIO library setup
GPIO.setwarnings(False)      #Turn off warnings

sensorSigFront1 = 23         #Front ultrasonic sensor 1 pin
sensorSigFront2 = 24         #Front ultrasonic sensor 2 pin
sensorSigSide1 = 2           #Side ultrasonic sensor 1 pin
sensorSigSide2 = 3           #Side ultrasonic sensor 2 pin

#Continuous loop
while True:

    GPIO.setup(sensorSigFront1, GPIO.OUT)       #Set front ultrasonic sensor 1 as output (trigger)
    GPIO.setup(sensorSigFront2, GPIO.OUT)       #Set front ultrasonic sensor 2 as output (trigger)
    GPIO.output(sensorSigFront1, True)          #Set front ultrasonic sensor 1 trigger ON
    GPIO.output(sensorSigFront2, True)          #Set front ultrasonic sensor 2 trigger ON
    sleep(0.00002)                              #Delay triggers for 2 microseconds
    GPIO.output(sensorSigFront1, False)         #Set front ultrasonic sensor 1 trigger OFF
    GPIO.output(sensorSigFront2, False)         #Set front ultrasonic sensor 2 trigger OFF
    GPIO.setup(sensorSigFront1, GPIO.IN)        #Set front ultrasonic sensor 1 as input (echo)
    GPIO.setup(sensorSigFront2, GPIO.IN)        #Set front ultrasonic sensor 2 as input (echo)
    
    while GPIO.input(sensorSigFront1) == False and GPIO.input(sensorSigFront2) == False:     #While the two front sensors echo are OFF
        pulse_start1 = time.time()                                                           #Record time at OFF, start of pulse
         
    while GPIO.input(sensorSigFront1) == True and GPIO.input(sensorSigFront2) == True:       #While the two front sensors echo are ON
        pulse_end1 = time.time()                                                             #Record time at ON, end of pulse
        
    pulse_duration1 = pulse_end1 - pulse_start1     #Calculate the time taken from start to end of pulse from front sensors

    distance1 = pulse_duration1 * 17000             #Calculate distance that pulse traveled, (time*(34000cm/s))/2 
    distance1 = round(distance1, 2)                 #Round distance to 2 decimal places

    GPIO.setup(sensorSigSide1, GPIO.OUT)       #Set side ultrasonic sensor 1 as output (trigger)
    GPIO.setup(sensorSigSide2, GPIO.OUT)       #Set side ultrasonic sensor 2 as output (trigger)
    GPIO.output(sensorSigSide1, True)          #Set side ultrasonic sensor 1 trigger ON
    GPIO.output(sensorSigSide2, True)          #Set side ultrasonic sensor 2 trigger ON
    sleep(0.00002)                             #Delay triggers for 2 microseconds
    GPIO.output(sensorSigSide1, False)         #Set side ultrasonic sensor 1 trigger OFF
    GPIO.output(sensorSigSide2, False)         #Set side ultrasonic sensor 2 trigger OFF
    GPIO.setup(sensorSigSide1, GPIO.IN)        #Set side ultrasonic sensor 1 as input (echo)
    GPIO.setup(sensorSigSide2, GPIO.IN)        #Set side ultrasonic sensor 2 as input (echo)

    while GPIO.input(sensorSigSide1) == False and GPIO.input(sensorSigSide2) == False:       #While the two side sensors echo are OFF
        pulse_start2 = time.time()                                                           #Record time at OFF, start of pulse
        
    while GPIO.input(sensorSigSide1) == True and GPIO.input(sensorSigSide2) == True:         #While the two side sensors echo are ON
        pulse_end2 = time.time()                                                             #Record time at ON, end of pulse
        
    pulse_duration2 = pulse_end2 - pulse_start2     #Calculate the time taken from start to end of pulse from side sensors

    distance2 = pulse_duration2 * 17000             #Calculate distance that pulse traveled, (time*(34000cm/s))/2
    distance2 = round(distance2, 2)                 #Round distance to 2 decimal places
    
    
    if distance1 > 2 and distance1 < 800:           #If front sensors distance is between 2 and 800 cm
        print "Distance1:", distance1,"cm"          #Display distance
        sleep(1)                                    #Delay for 1 second

    if distance2 > 2 and distance2 < 800:           #If front sensors distance is between 2 and 800 cm
        print "Distance2:", distance2,"cm"          #Display distance
        sleep(1)                                    #Delay for 1 second

    else:
        print "Out of Range"                        #Otherwise, sensor out of range of objects

