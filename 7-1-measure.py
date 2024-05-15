import RPi.GPIO as GPIO # type: ignore
import matplotlib.pyplot as plt # type: ignore
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
	return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
	b = 0
	for i in range(7, -1, -1):
		b += 2**i
		val = decimal2binary(b)
		GPIO.output(dac, val)
		time.sleep(0.01)
		cmp = GPIO.input(comp)
		if cmp == 1:
			b -= 2**i
	return b

GPIO.output(troyka, 1)

values = []
times = []

try:
	begin = time.time()
	value = 0

	while value < 210:
		value = adc()
		print(" volts up - {:3}".format(value / 2**8 * 3.3))
		GPIO.output(dac, decimal2binary(value))
		values.append(value)
		times.append(time.time() - begin)

	GPIO.output(troyka, 0)

	while (value > 168):
		value = adc()
		print(" volts down - {:3}".format(value / 2**8 * 3.3))
		GPIO.output(dac, decimal2binary(value))
		values.append(value)
		times.append(time.time() - begin)

	end = time.time()

	with open("settings.txt", "w") as output:
		output.write(str((end - begin) / len(values)))
		output.write(("\n"))
		output.write(str(3.3 / 256))

	print(end - begin)
	print(len(values) / (end - begin))
	print((end - begin) / len(values))
	print(3.3 / 256)

finally:
	GPIO.output(dac, GPIO.LOW)
	GPIO.output(troyka, GPIO.LOW)
	GPIO.cleanup()

value_str = [str(data) for data in values]

with open("data.txt", "w") as output:
	output.write("\n".join(value_str))

plt.plot(times, values)
plt.show()