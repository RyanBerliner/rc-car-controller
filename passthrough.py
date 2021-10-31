import RPi.GPIO as GPIO
import time

print('start')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.OUT)

servo = GPIO.PWM(11, 50)
servo.start(0)

try:
    while True:
        start = time.time()
        stop = time.time()

        while GPIO.input(7) == 0:
            start = time.time()
        while GPIO.input(7) == 1:
            pass

        stop = time.time()
        val = (stop - start) * 1000 - 1
        # the servo i'm testing has valid duty cycle of 5 -> 9.5
        cycle = 4.5 * val + 5
        print(cycle)
        servo.ChangeDutyCycle(cycle)
finally:
    servo.stop()
    GPIO.cleanup()
    print('stop')
