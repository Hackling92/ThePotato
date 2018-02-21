import RPi.GPIO as GPIO
import time
#                a,b,c, d, e, f, g, a, b, c, d, e, f, g
chan_list_out = [3,5,7,29,31,26,24,21,19,23,32,33,36,11]
chan_list_in  = [12,35,38,40]

HI_MSG = [31,26,19,23,33,36,11]
ZERO =   [3,5,7,29,31,26]
ONE =    [5,7]
TWO =    [3,5,29,31,24]

def blank(): GPIO.output(chan_list_out,GPIO.LOW)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(chan_list_out, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(chan_list_in , GPIO.IN , pull_up_down=GPIO.PUD_UP)

GPIO.output(HI_MSG, GPIO.HIGH)

while(True):

    if(GPIO.input(12) == 0):
        # button 1
        blank()
        GPIO.output(ZERO, GPIO.HIGH)
    if(GPIO.input(35) == 0):
        # button 2
        blank()
        GPIO.output(ONE, GPIO.HIGH)
    if(GPIO.input(38) == 0):
        # button 3
        blank()
        GPIO.output(TWO, GPIO.HIGH)
    if(GPIO.input(40) == 0):
        # button 4
        break;
    
    time.sleep(0.01)

    
GPIO.cleanup(chan_list_out)
GPIO.cleanup(chan_list_in)
