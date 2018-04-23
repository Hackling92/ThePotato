import RPi.GPIO as GPIO
import time


DEBOUNCE_INTERVAL = 150

inputPins = [32,22,12,33]
outputPins = [11,13,15,19,21,23,29,31,35,37,40,38,36]

buttons = {1: 32, 2: 22, 3: 12, 4: 33}

global leftCnt
global rightCnt
leftCnt = 0
rightCnt = 0
leftTestData = ['0','1','7','u','n']
rightTestData = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']



segToPin = {'la': 15, 'lb': 19, 'lc': 35, 'ld': 13, 'le': 31, 'lf': 11, 'ra': 23, 'rb': 29, 'rc': 36, 'rd': 40, 're': 37, 'rf': 21, 'rg': 38}
disp = {'left':{'0': [segToPin['la'],segToPin['lb'],segToPin['lc'],segToPin['ld'],segToPin['le'],segToPin['lf']],
		'1': [segToPin['lb'],segToPin['lc']],
		'7': [segToPin['la'],segToPin['lb'],segToPin['lc']],
		'u': [segToPin['lb'],segToPin['lc'],segToPin['ld'],segToPin['le'],segToPin['lf']],
		'n': [segToPin['la'],segToPin['lb'],segToPin['lc'],segToPin['le'],segToPin['lf']],
		'blank': [segToPin['la'],segToPin['lb'],segToPin['lc'],segToPin['ld'],segToPin['le'],segToPin['lf']]},
	'right':{'0': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf']],
		'1': [segToPin['rb'],segToPin['rc']],
		'2': [segToPin['ra'],segToPin['rb'],segToPin['rd'],segToPin['re'],segToPin['rg']],
		'3': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['rg']],
		'4': [segToPin['rb'],segToPin['rc'],segToPin['rf'],segToPin['rg']],
		'5': [segToPin['ra'],segToPin['rc'],segToPin['rd'],segToPin['rf'],segToPin['rg']],
		'6': [segToPin['ra'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
		'7': [segToPin['ra'],segToPin['rb'],segToPin['rc']],
		'8': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
		'9': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rf'],segToPin['rg']],
		'a': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['re'],segToPin['rf'],segToPin['rg']],
		'b': [segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
		'c': [segToPin['ra'],segToPin['rd'],segToPin['re'],segToPin['rf']],
		'd': [segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rg']],
		'e': [segToPin['ra'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
		'f': [segToPin['ra'],segToPin['re'],segToPin['rf'],segToPin['rg']],
		'blank': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']]}}




# Name: printSegment
# pos is left right or both displays
# left character (0,1,7,u,n)
# right character (0-9, a-f)
def printSegment(pos, char):
	if(pos == 'both'):
		GPIO.output(disp['left']['blank'], GPIO.LOW)
		GPIO.output(disp['right']['blank'], GPIO.LOW)
		GPIO.output(disp['left'][char[0]], GPIO.HIGH)
		GPIO.output(disp['right'][char[1]], GPIO.HIGH)
	elif(pos == 'left'):
		GPIO.output(disp['left']['blank'], GPIO.LOW)
		GPIO.output(disp['left'][char], GPIO.HIGH)
	elif(pos == 'right'):
		GPIO.output(disp['right']['blank'], GPIO.LOW)
		GPIO.output(disp['right'][char], GPIO.HIGH)


def leftUp(channel):
	print("Left Up Pressed")
	global leftCnt
	leftCnt = (leftCnt + 1) % 5
	printSegment('left', leftTestData[leftCnt])

def leftDown(channel):
	print("Left Down Pressed")
	global leftCnt
	leftCnt = (leftCnt - 1) % 5
	printSegment('left', leftTestData[leftCnt])

def RightUp(channel):
	print("Right Up Pressed")
	global rightCnt
	rightCnt = (rightCnt + 1) % 16
	printSegment('right', rightTestData[rightCnt])


def RightDown(channel):
	print("Right Down Pressed")
	global rightCnt
	rightCnt = (rightCnt - 1) % 16
	printSegment('right', rightTestData[rightCnt])


# example of how to print 2 characters at the same time
#printSegment('both', rightTestData[0] + rightTestData[rightCnt - 1])



def main():

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD) # set gpio pin numbers to board numbers
	GPIO.setup(outputPins, GPIO.OUT) # set all led pins as outputs
	GPIO.setup(inputPins, GPIO.IN, pull_up_down = GPIO.PUD_UP) # set all buttons as inputs with pullup resistors

	#for x in leftTestData:
	#	GPIO.output(disp['left']['blank'], GPIO.LOW)
	#	GPIO.output(disp['left'][x], GPIO.HIGH)
	#	time.sleep(0.1)

	#for x in rightTestData:
	#	GPIO.output(disp['right']['blank'], GPIO.LOW)
	#	GPIO.output(disp['right'][x], GPIO.HIGH)
	#	time.sleep(0.1)


	GPIO.output(disp['left']['blank'], GPIO.LOW)	# clear any old segments
	GPIO.output(disp['right']['blank'], GPIO.LOW)	# clear any old segments

	# register each button press as an event (also adds debouncing)
	GPIO.add_event_detect(buttons[1], GPIO.FALLING, callback=leftUp, bouncetime=DEBOUNCE_INTERVAL)
	GPIO.add_event_detect(buttons[2], GPIO.FALLING, callback=leftDown, bouncetime=DEBOUNCE_INTERVAL)
	GPIO.add_event_detect(buttons[3], GPIO.FALLING, callback=RightUp, bouncetime=DEBOUNCE_INTERVAL)
	GPIO.add_event_detect(buttons[4], GPIO.FALLING, callback=RightDown, bouncetime=DEBOUNCE_INTERVAL)


	try:
		# this is where the real vehicle program goes
		while True:
			time.sleep(0.001)

	finally:
		GPIO.cleanup()

main()
