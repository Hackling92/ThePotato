from evdev import InputDevice, categorize, ecodes, KeyEvent
gamepad = InputDevice('/dev/input/event0')

#Button Code
LTrig= 292
RTrig= 293

Xbutton= 288
Ybutton= 291
Abutton= 289
Bbutton= 290

select= 296
start= 297


for event in gamepad.read_loop():
	if event.type == ecodes.EV_KEY:
		if event.type == 1: 
			if event.code == Xbutton: # keyevent.keycode =='BTN_JOYSTICK':
				print "Left Motor Forward"
			elif event.code == Ybutton: #keyevent.keycode == 'BTN_TOP':
				print "Left Motor Backward"
			elif event.code == Abutton: #keyevent.keycode == 'BTN_THUMB':
				print "Right Motor Forward"
			elif event.code == Bbutton: #keyevent.keycode == 'BTN_THUMB2':
				print "Right Motor Backward"
			elif event.code == LTrig: #keyevent.keycode == 'BTN_PINKIE':
				print "Stop iRobot"
                                
			
