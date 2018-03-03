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

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

axisAservo = 0;
axisBservo = 1;
axisCservo = 2;
axisDservo = 3;
axisEservo = 4;

axisAservoMin =  150;
axisAservoMax =  600;
axisBservoMin =  150;
axisBservoMax =  600;
axisCservoMin =  150;
axisCservoMax =  600;
axisDservoMin =  150;
axisDservoMax =  600;
axisEservoMin =  150;
axisEservoMax =  600;


def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

  def main():
	pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
	# while (True):
	  # pwm.setPWM(0, 0, servoMin)
	  # time.sleep(1)
	  # pwm.setPWM(0, 0, servoMax)
	  # time.sleep(1)

	for event in gamepad.read_loop():
    #Boutons | buttons 
    if event.type == ecodes.EV_KEY:
        #print(event)
        if event.value == 1:
            if event.code == xBtn:
                print("X")
            elif event.code == bBtn:
                print("B")
            elif event.code == aBtn:
                print("A")
            elif event.code == yBtn:
                print("Y")
            elif event.code == lBtn:
                print("l_shoulder")
            elif event.code == rBtn:
                print("r_shoulder")
            elif event.code == selBtn:
                print("Select")
            elif event.code == staBtn:
                print("Start")
        elif event.value == 0:
          print("Release")

    #Gamepad analogique | Analog gamepad
    elif event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        #print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X":
             if absevent.event.value == 0:
                print("Left")
             elif absevent.event.value == 255:
                print("Right")
             elif absevent.event.value == 127:
                print("Center")
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
             if absevent.event.value == 0:
                print("Up")
             elif absevent.event.value == 255:
                print("Down")
             elif absevent.event.value == 127:
                print("Center")

if __name__ == "__main__":
    main()
 