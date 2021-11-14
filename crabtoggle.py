from multiprocessing import Process, Value
from collections import deque
from statistics import mean
import RPi.GPIO as GPIO
import time


class PWM_Reader:
    def __init__(self, pin, max_update_frequency=None, smoothing=False):
        self.pin = pin
        self.read_process = None
        self.max_update_frequency = max_update_frequency
        self.smoothing = smoothing
        GPIO.setup(self.pin, GPIO.IN)

    def start_reading(self):
        if self.read_process is not None:
            return

        value = Value('d', 0.0)

        self.read_process = Process(target=self.read, args=(value, self.max_update_frequency, self.smoothing))
        self.read_process.start()

        return lambda : value.value

    def stop_reading(self):
        self.read_process.terminate()
        self.read_process = None

    def read(self, v, max_update_frequency, smoothing):
        previous_raw_values = deque(maxlen=20)

        while True:
            start = time.time()
            stop = time.time()
            while GPIO.input(self.pin) == 0:
                start = time.time()
            while GPIO.input(self.pin) == 1:
                pass
            stop = time.time()
            # typically a value between 0 and 1
            val = (stop - start) * 1000 - 1
            previous_raw_values.append(val)
            smoothed = mean(previous_raw_values) if smoothing else val
            v.value = smoothed

            if max_update_frequency is not None:
                time.sleep(1.0 / max_update_frequency)


    
def run():
    print('start')

    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(11, GPIO.OUT)
    servo = GPIO.PWM(11, 50)
    servo.start(0)

    steering_reader = PWM_Reader(7, smoothing=True)
    mode_reader = PWM_Reader(15, max_update_frequency=1)

    s_val = steering_reader.start_reading()
    m_val = mode_reader.start_reading()

    SERVO_DC_HIGH = 9.5
    SERVO_DC_LOW = 5.0

    try:
        last_action_cycle = last_cycle = (SERVO_DC_HIGH + SERVO_DC_LOW) / 2.0
        last_action = time.time()
        mode = False

        while True:
            sv = s_val()
            mv = m_val()

            if sv is None:
                continue

            mv = mv > 0.5
            diff = SERVO_DC_HIGH - SERVO_DC_LOW
            middle = (SERVO_DC_HIGH + SERVO_DC_LOW) / 2.0
            val = diff * sv + SERVO_DC_LOW
            cycle = val if mv else middle - val + middle
            cycle_diff = abs(last_action_cycle - cycle)

            # only respond to significant changes
            if  (cycle_diff > 0.1 and cycle_diff < 0.75) or mode != mv:
                mode = mv
                last_action_cycle = cycle
                last_cycle = cycle
                last_action = time.time()
                servo.ChangeDutyCycle(cycle)
                print('signal move %f in mode %i' % (cycle, 1 if mv else 0))
            elif last_cycle != 0 and time.time() - last_action > 1:
                print('signal pause')
                last_cycle = 0
                servo.ChangeDutyCycle(0)


    finally:
        steering_reader.stop_reading()
        mode_reader.stop_reading()
        GPIO.cleanup()

        print('stopped')


if __name__ == '__main__':
    run()
