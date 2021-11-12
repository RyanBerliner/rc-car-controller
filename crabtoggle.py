import RPi.GPIO as GPIO
import time
import threading

class PWM_Reader:
    def __init__(self, pin):
        self.pin = pin
        self.reading = False
        self.last_value = None
        GPIO.setup(self.pin, GPIO.IN)

    def start_reading(self):
        if (self.reading):
            return

        self.reading = True
        read_thread = threading.Thread(target=self.read)
        read_thread.start()

    def stop_reading(self):
        self.reading = False

    def read(self):
         while(self.reading):
            start = time.time()
            stop = time.time()
            while GPIO.input(self.pin) == 0:
                start = time.time()
            while GPIO.input(self.pin) == 1:
                pass
            stop = time.time()
            self.last_value = stop - start 

    
def run():
    print('start')

    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(11, GPIO.OUT)
    servo = GPIO.PWM(11, 50)
    servo.start(0)

    steering_reader = PWM_Reader(7)
    mode_reader = PWM_Reader(15)
    
    steering_reader.start_reading()
    # mode_reader.start_reading()

    try:
        while True:
            if steering_reader.last_value is None:
                continue
            val = steering_reader.last_value  * 1000 - 1
            # the servo i'm testing has valid duty cycle of 5 -> 9.5
            cycle = 4.5 * val + 5
            print(cycle)
            servo.ChangeDutyCycle(cycle)
    finally:
        steering_reader.stop_reading()
        mode_reader.stop_reading()
        GPIO.cleanup()

        print('stopped')


if __name__ == '__main__':
    run()
