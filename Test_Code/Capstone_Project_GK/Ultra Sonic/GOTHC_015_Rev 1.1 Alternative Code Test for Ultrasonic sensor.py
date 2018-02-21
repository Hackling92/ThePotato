import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sensorSig1 = 24
sensorSig2 = 23

while True:

    GPIO.setup(sensorSig1, GPIO.OUT)
    GPIO.setup(sensorSig2, GPIO.OUT)
    GPIO.output(sensorSig1, True)
    GPIO.output(sensorSig2, True)
    sleep(0.00002)
    GPIO.output(sensorSig1, False)
    GPIO.output(sensorSig2, False)
    GPIO.setup(sensorSig1, GPIO.IN)
    GPIO.setup(sensorSig2, GPIO.IN)
    
    while GPIO.input(sensorSig1) == False and GPIO.input(sensorSig2) == False:
        pulse_start = time.time()
        
    while GPIO.input(sensorSig1) == True and GPIO.input(sensorSig2) == True:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17000
    distance = round(distance, 2)
    
    if distance > 2 and distance < 800:
        print "Distance:", distance,"cm"
        sleep(1)
    else:
        print "Out of Range"
