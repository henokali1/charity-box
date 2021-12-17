# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
motForward = 23 # Broadcom pin 18 (P1 pin 12)
motReverse = 24 # Broadcom pin 23 (P1 pin 16)

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(motReverse, GPIO.OUT) 
GPIO.setup(motForward, GPIO.OUT) 

# Initial state for LEDs:
GPIO.output(motReverse, GPIO.LOW)
GPIO.output(motForward, GPIO.LOW)

def motorForward():
    print('motorForward\t\tmotForward:HIGH\tmotReverse:LOW')
    GPIO.output(motForward, GPIO.HIGH)
    GPIO.output(motReverse, GPIO.LOW)
    time.sleep(10)

def motorReverse():
    print('motorReverse\t\tmotForward:LOW\tmotReverse:HIGH')
    GPIO.output(motForward, GPIO.LOW)
    GPIO.output(motReverse, GPIO.HIGH)
    time.sleep(10)

def motorOff():
    print('motorOff\t\tmotForward:LOW\tmotReverse:LOW')
    GPIO.output(motForward, GPIO.LOW)
    GPIO.output(motReverse, GPIO.LOW)

print("Motor Test! Press CTRL+C to exit")
try:
    while 1:
        motorForward()
        motorOff()
        time.sleep(5)
        motorReverse()
        motorOff()
        time.sleep(5)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    motorOff()
    GPIO.cleanup() # cleanup all GPIO
