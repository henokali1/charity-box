from __future__ import print_function
import RPi.GPIO as GPIO
import qwiic_serlcd
import qwiic_keypad
import threading
import time
import sys


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 20
GPIO_ECHO = 21
motForward = 23
motReverse = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(motReverse, GPIO.OUT) 
GPIO.setup(motForward, GPIO.OUT) 

# Initial state for LEDs:
GPIO.output(motReverse, GPIO.LOW)
GPIO.output(motForward, GPIO.LOW)
MOTOR_DELAY = 3
RUN_THREAD = True
myLCD = qwiic_serlcd.QwiicSerlcd()
distance = 0
box_height = 100


def motorForward():
	print('motorReverse\t\tmotForward:LOW\tmotReverse:HIGH')
	GPIO.output(motForward, GPIO.LOW)
	GPIO.output(motReverse, GPIO.HIGH)
	time.sleep(MOTOR_DELAY)
	motorOff()

def motorReverse():
	print('motorForward\t\tmotForward:HIGH\tmotReverse:LOW')
	GPIO.output(motForward, GPIO.HIGH)
	GPIO.output(motReverse, GPIO.LOW)
	time.sleep(MOTOR_DELAY)
	motorOff()

def motorOff():
	print('motorOff\t\tmotForward:LOW\tmotReverse:LOW')
	GPIO.output(motForward, GPIO.LOW)
	GPIO.output(motReverse, GPIO.LOW)
 
def update_distance(name):
	global distance
	while RUN_THREAD:
		# set Trigger to HIGH
		GPIO.output(GPIO_TRIGGER, True)
	
		# set Trigger after 0.01ms to LOW
		time.sleep(0.00001)
		GPIO.output(GPIO_TRIGGER, False)
	
		StartTime = time.time()
		StopTime = time.time()
	
		# save StartTime
		while GPIO.input(GPIO_ECHO) == 0:
			StartTime = time.time()
	
		# save time of arrival
		while GPIO.input(GPIO_ECHO) == 1:
			StopTime = time.time()
	
		# time difference between start and arrival
		TimeElapsed = StopTime - StartTime
		# multiply with the sonic speed (34300 cm/s)
		# and divide by 2, because there and back
		distance = int((TimeElapsed * 34300) / 2)
		percentage = _map(distance, 0, box_height, 100, 0)
		print(f'Distance: {distance}cm\t\t {percentage}% full')
		time.sleep(1) 


keys_prsd = ''

def _map(x, in_min, in_max, out_min, out_max):
	return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def main_rn():
	global keys_prsd
	myKeypad = qwiic_keypad.QwiicKeypad(0x4b)

	

	if myLCD.connected == False:
		print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	if myKeypad.is_connected() == False:
		print("The Qwiic Keypad device isn't connected to the system. Please check your connection", file=sys.stderr)
		return

	myKeypad.begin()

	button = 0

	myLCD.setBacklight(255, 255, 255) # Set backlight to bright white
	myLCD.setContrast(5) # set contrast. Lower to 0 for higher contrast.
	myLCD.clearScreen() # clear the screen - this moves the cursor to the home position as well

	time.sleep(1) # give a sec for system messages to complete
	
	myLCD.print("Enter Pin")
	while True:
		try:
			myKeypad.update_fifo()
		except:
			pass
		button = myKeypad.get_button()

		if button == -1:
			print("No keypad detected")
			time.sleep(1)
		elif button != 0:
			# Get the character version of this char
			charButton = chr(button)
			if charButton == '#':
				if keys_prsd == '1111' or keys_prsd == '0000':
					print(keys_prsd)
					keys_prsd = ''
					print()
					myLCD.clearScreen()
					myLCD.setCursor(0,0)
					myLCD.print("Please Wait")
					myLCD.setCursor(0,1)
					myLCD.print("Closing....")
					motorReverse()
					myLCD.clearScreen()
					myLCD.setCursor(0,0)
					myLCD.print("Enter Pin")
				else:
					print(keys_prsd)
					print()
					print(keys_prsd)
					keys_prsd = ''
					print()
					myLCD.clearScreen()
					myLCD.setCursor(0,0)
					myLCD.print("Access Granted")
					myLCD.setCursor(0,1)
					myLCD.print("Unlocking....")
					motorForward()
					
					myLCD.clearScreen()
					myLCD.setCursor(0,0)
					myLCD.print("Enter Pin")


			elif charButton == '*':
				print("*", end="")
			else:
				keys_prsd +=  charButton
				print(charButton, end="")
				myLCD.setCursor(0,1)
				myLCD.print('*'*len(keys_prsd))

			# Flush the stdout buffer to give immediate user feedback
			sys.stdout.flush()
		time.sleep(.25)

if __name__ == '__main__':
	try:
		distance_thread = threading.Thread(target=update_distance, args=(1,))
		distance_thread.start()
		while True:
			# dist = int(distance())
			# print (f"Measured Distance = {dist}cm")
			# time.sleep(1)
			main_rn()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding")
		myLCD.clearScreen()
		motorOff()
		GPIO.cleanup()
		sys.exit(0)
		
