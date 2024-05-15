import RPi.GPIO as GPIO # type: ignore
from time import sleep

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
	return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
	b = 0
	for i in range(7, -1, -1):
		b += 2**i
		val = decimal2binary(b)
		GPIO.output(dac, val)
		sleep(0.01)
		cmp = GPIO.input(comp)
		if cmp:
			b -= 2**i	
	return b

try:
	while True:
		dig_val = adc()
		if dig_val:
			val = int(dig_val / 256 * 10)
			lst = [0]*8
			for i in range (val - 1):
				lst[i] = 1
			GPIO.output(leds, lst)
			print(val)
finally:
	GPIO.output(dac, 0)
	GPIO.cleanup()