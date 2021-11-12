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
            print(self.last_value)

    
def run():
    print('start')

    GPIO.setmode(GPIO.BOARD)

    reader1 = PWM_Reader(7)
    reader2 = PWM_Reader(15)
    
    time.sleep(5)
    reader1.start_reading()
    reader2.start_reading()

    time.sleep(5)
    reader1.stop_reading()
    reader2.stop_reading()

    time.sleep(5)
    GPIO.cleanup()
    print('stop')

if __name__ == '__main__':
    run()
