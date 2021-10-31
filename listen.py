import RPi.GPIO as GPIO
import time

print('start')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

# https://forums.raspberrypi.com/viewtopic.php?t=48592

try:
    while True:
        start = time.time()
        stop = time.time()

        while GPIO.input(7) == 0:
            start = time.time()
        while GPIO.input(7) == 1:
            pass

        stop = time.time()
        print(stop - start)
finally:
    GPIO.cleanup()
    print('stop')
