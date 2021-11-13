from multiprocessing import Process, Value
import RPi.GPIO as GPIO
import time

class PWM_Reader:
    def __init__(self, pin, max_update_frequency=None):
        self.pin = pin
        self.read_process = None
        self.max_update_frequency = max_update_frequency
        GPIO.setup(self.pin, GPIO.IN)

    def start_reading(self):
        if self.read_process is not None:
            return

        value = Value('d', 0.0)

        self.read_process = Process(target=self.read, args=(value, self.max_update_frequency))
        self.read_process.start()

        return lambda : value.value

    def stop_reading(self):
        self.read_process.terminate()
        self.read_process = None

    def read(self, v, max_update_frequency):
        while True:
            start = time.time()
            stop = time.time()
            while GPIO.input(self.pin) == 0:
                start = time.time()
            while GPIO.input(self.pin) == 1:
                pass
            stop = time.time()
            # typically a value between 0 and 1
            v.value = (stop - start) * 1000 - 1

            if max_update_frequency is not None:
                time.sleep(1.0 / max_update_frequency)


    
def run():
    print('start')

    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(11, GPIO.OUT)
    servo = GPIO.PWM(11, 50)
    servo.start(0)

    steering_reader = PWM_Reader(7)
    mode_reader = PWM_Reader(15, max_update_frequency=1)

    s_val = steering_reader.start_reading()
    m_val = mode_reader.start_reading()

    SERVO_DC_HIGH = 9.5
    SERVO_DC_LOW = 5.0

    try:
        while True:
            if s_val() is None:
                continue
            diff = SERVO_DC_HIGH - SERVO_DC_LOW
            middle = (SERVO_DC_HIGH + SERVO_DC_LOW) / 2.0
            val = diff * s_val() + SERVO_DC_LOW
            cycle = val if m_val() > 0.5 else middle - val + middle
            servo.ChangeDutyCycle(cycle)
    finally:
        steering_reader.stop_reading()
        mode_reader.stop_reading()
        GPIO.cleanup()

        print('stopped')


if __name__ == '__main__':
    run()
