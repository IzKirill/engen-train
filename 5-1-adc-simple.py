import RPi.GPIO as GPIO # type: ignore
from time import sleep

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
	return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
	for i in range(256):
		val = decimal2binary(i)
		GPIO.output(dac, val)
		cmp = GPIO.input(comp)
		sleep(0.01)
		if cmp:
			return i
	return 0

try:
	while True:
		dig_val = adc()
		voltage = (dig_val / 255.0) * 3.3
		if dig_val:
			print("{:.4f}".format(voltage))

finally:
	GPIO.output(dac, 0)
	GPIO.clear()