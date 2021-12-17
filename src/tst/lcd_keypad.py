from __future__ import print_function
import qwiic_serlcd
import qwiic_keypad
import time
import sys


keys_prsd = ''
def main_rn():
	global keys_prsd
	myKeypad = qwiic_keypad.QwiicKeypad(0x4b)

	myLCD = qwiic_serlcd.QwiicSerlcd()

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
				print()
				print(keys_prsd)
				keys_prsd = ''
				print()
				myLCD.clearScreen()
				myLCD.setCursor(0,0)
				myLCD.print("Access Granted")
				myLCD.setCursor(0,1)
				myLCD.print("Unlocking....")
			elif charButton == '*':
				print(" ", end="")
			else:
				keys_prsd +=  charButton
				print(charButton, end="")
				myLCD.setCursor(0,1)
				myLCD.print(keys_prsd)

			# Flush the stdout buffer to give immediate user feedback
			sys.stdout.flush()

		time.sleep(.25)

if __name__ == '__main__':
	try:
		main_rn()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding")
		sys.exit(0)
