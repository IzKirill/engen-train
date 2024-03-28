import RPi.GPIO as GPIO

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
return [int(bit) for bit in bin(value)[2:].zfill(8)]

try:
while True:
val = input("Input value: ")
if val == "q":
break
try:
    val = int(val)
    if 0 <= val <= 255:
        GPIO.output(dac, decimal2binary(val))
        u = (float(val) / 256.0) * 3.3
        print("{:.4f}".format(u))
    else:
        if val < 0:
        print("You input valueй less zero, incorrect")
        elif val > 255:
        print("You input value bigger than 255, incorrect")
    except Exception:   
    print("You input string, incorrect")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()