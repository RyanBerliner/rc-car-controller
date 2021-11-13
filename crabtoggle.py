from multiprocessing import Process, Value
import RPi.GPIO as GPIO
import time

class PWM_Reader:
    def __init__(self, pin):
        self.pin = pin
        self.read_process = None
        GPIO.setup(self.pin, GPIO.IN)

    def start_reading(self):
        if self.read_process is not None:
            return

        value = Value('d', 0.0)

        self.read_process = Process(target=self.read, args=(value,))
        self.read_process.start()

        return lambda : value.value

    def stop_reading(self):
        self.read_process.terminate()
        self.read_process = None

    def read(self, v):
        while True:
            start = time.time()
            stop = time.time()
            while GPIO.input(self.pin) == 0:
                start = time.time()
            while GPIO.input(self.pin) == 1:
                pass
            stop = time.time()
            v.value = stop - start

    
def run():
    print('start')

    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(11, GPIO.OUT)
    servo = GPIO.PWM(11, 50)
    servo.start(0)

    steering_reader = PWM_Reader(7)
    mode_reader = PWM_Reader(15)

    s_val = steering_reader.start_reading()
    m_val = mode_reader.start_reading()

    try:
        while True:
            if s_val() is None:
                continue
            val = s_val()  * 1000 - 1
            # the servo i'm testing has valid duty cycle of 5 -> 9.5
            cycle = 4.5 * val + 5
            servo.ChangeDutyCycle(cycle)
    finally:
        steering_reader.stop_reading()
        mode_reader.stop_reading()
        GPIO.cleanup()

        print('stopped')


if __name__ == '__main__':
    run()
