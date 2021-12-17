import qwiic_keypad
import time
import sys

# print("\nSparkFun qwiic Keypad   Example 1\n")
# myKeypad = qwiic_keypad.QwiicKeypad(0x4b)
# if myKeypad.is_connected() == False:
# 	print("The Qwiic Keypad device isn't connected to the system. Please check your connection", file=sys.stderr)
# myKeypad.begin()
# button = 0

keys_prsd = ''
def keypad_st():
	global keys_prsd

	myKeypad = qwiic_keypad.QwiicKeypad(0x4b)
	if myKeypad.is_connected() == False:
		print("The Qwiic Keypad device isn't connected to the system. Please check your connection", file=sys.stderr)
		return

	myKeypad.begin()

	button = 0
	while True:

		# necessary for keypad to pull button from stack to readable register
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
			elif charButton == '*':
				print(" ", end="")
			else:
				keys_prsd +=  charButton
				print(charButton, end="")

			# Flush the stdout buffer to give immediate user feedback
			sys.stdout.flush()

		time.sleep(.25)
		# Development in progress
keypad_st()