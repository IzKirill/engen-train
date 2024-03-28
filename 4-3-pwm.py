import RPi.GPIO as GPIO

n = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(n, GPIO.OUT)

p = GPIO.PWM(n, 1000)
p.start(0)

try:
	while True:
		val = int(input("Input value: "))
		p.ChangeDutyCycle(val)
		print(3.3 * val / 100)

finally:
	p.stop()
	GPIO.cleanup()