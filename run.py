import RPi.GPIO as GPIO
import time

print('start')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
servo = GPIO.PWM(7, 50)
servo.start(0)

try:
    while True:
        cycle = float(input('enter duty cycle value: '))
        servo.ChangeDutyCycle(cycle)
finally:
    servo.stop()
    GPIO.cleanup()
    print('stop')
