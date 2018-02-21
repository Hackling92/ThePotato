import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)
print "LED ON"
GPIO.output(14,GPIO.HIGH)
time.sleep(10)
print "LED OFF"
GPIO.output(14,GPIO.LOW)
