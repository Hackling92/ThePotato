import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sensorSig = 24

while True:

    GPIO.setup(sensorSig, GPIO.OUT)
    GPIO.output(sensorSig, True)
    sleep(0.00002)
    GPIO.output(sensorSig, False)
    GPIO.setup(sensorSig, GPIO.IN)

    
    while GPIO.input(sensorSig) == False:
        pulse_start = time.time()
        
    while GPIO.input(sensorSig) == True:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17000
    distance = round(distance, 2)
    
    if distance > 2 and distance < 800:
        print "Distance:", distance,"cm"
        sleep(1)
    else:
        print "Out of Range"
