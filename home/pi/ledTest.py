import RPi.GPIO as GPIO
import time
# Set GPIO pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, True)
time.sleep(20)
GPIO.output(18, False)