import RPi.GPIO as GPIO
from time import sleep

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

try:
    val = 0
    up = 1
    T = float(input("Input period: "))

    while True:
        GPIO.output(dac, decimal2binary(val))
        if val == 255: up = 0
        if (val == 0 and up == 0): up = 1

        if up == 1: val = val + 1
        else: val = val - 1

        sleep(T / 512)

except ValueError:
    print("You input incorrect period, please try again ")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()()