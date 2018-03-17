#!/usr/bin/python

###
# 
#  Work in Progress
#
###

from Adafruit_PWM_Servo_Driver import PWM
#import evdev
from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice('/dev/input/event0')

#print(gamepad)

# Gamepad Buttons
aBtn = 289
bBtn = 290
xBtn = 288
yBtn = 291
lBtn = 292
rBtn = 293
selBtn = 296
staBtn = 297

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)



axisStor =  [
		# [axisCh, axisMin, axisMax, axisPos, defaultStep]
		[0, 150, 650, 370, 15], # 0 / A
		[1, 150, 650, 370, 15], # 1 / B
		[2, 150, 650, 370, 15], # 2 / C
		[3, 150, 650, 370, 15], # 3 / D
		[4, 150, 650, 370, 15], # 4 / E
	]


# def setServoPulse(channel, pulse):
  # # pulseLength = 1000000                   # 1,000,000 us per second
  # # pulseLength /= 60                       # 60 Hz
  # # print "%d us per period" % pulseLength
  # # pulseLength /= 4096                     # 12 bits of resolution
  # # print "%d us per bit" % pulseLength
  # pulseLength = 4.0690104166666666666666666666667
  # pulse *= 1000
  # pulse /= pulseLength
  # pwm.setPWM(channel, 0, pulse)
  
	
def moveAxis(axis, step):
	if 0 <= axis <= 4:
		newPulse = axisStor[axis][3]
		newPulse += step
		if axisStor[axis][1] > newPulse:
			newPulse = axisStor[axis][1]
		elif axisStor[axis][2] < newPulse:
			newPulse = axisStor[axis][2]
			# update pulse in storage
		axisStor[axis][3] = newPulse
		# write pulse to servo
		pwm.setPWM(axisStor[axis][0], 0, axisStor[axis][3])
		print "axis channel %d " % axisStor[axis][0]
		print "step %d " % step
		print "new Pulse is %d " % axisStor[axis][3]


def main():
	pwm.setPWMFreq(60)   # Set frequency to 60 Hz
	for event in gamepad.read_loop():
	  # buttons 
	  if event.type == ecodes.EV_KEY:
		#print(event)
		if event.value == 1:
			if event.code == xBtn:                
			  moveAxis(2, axisStor[2][4])
			  print("X")
			elif event.code == bBtn:                
			  moveAxis(2, axisStor[2][4] * -1)
			  print("B")
			elif event.code == aBtn:
			  print("A")
			elif event.code == yBtn:
				print("Y")
			elif event.code == lBtn:			                
			  moveAxis(3, axisStor[3][4])
			  print("l_shoulder")
			elif event.code == rBtn:			                
			  moveAxis(3, axisStor[3][4] * -1)
			  print("r_shoulder")
			elif event.code == selBtn:			                
			  moveAxis(4, axisStor[4][4])
			  print("Select")
			elif event.code == staBtn:			                
			  moveAxis(4, axisStor[4][4] * -1)
			  print("Start")
		elif event.value == 0:
		  print("Release")

	  # Analog gamepad
	  elif event.type == ecodes.EV_ABS:
		absevent = categorize(event)
		#print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
		if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X":
		  if absevent.event.value == 0:			 			                
			moveAxis(0, axisStor[0][4])
			print("Left")
		  elif absevent.event.value == 255: 			                
			moveAxis(0, axisStor[0][4] * -1)
			print("Right")
		  elif absevent.event.value == 127:
			print("Center")
		elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
			if absevent.event.value == 0:	 			                
			  moveAxis(1, axisStor[1][4])
			  print("Up")
			elif absevent.event.value == 255:		                
			  moveAxis(1, axisStor[1][4] * -1)
			  print("Down")
			elif absevent.event.value == 127:
			  print("Center")

if __name__ == "__main__":
    main()
 