import numpy as np
from struct import pack
from collections import defaultdict, deque
from queue import Queue
from functools import partial
from serial import Serial
from time import sleep, time
from threading import Thread, Lock
from defaults import max_recorded, samplefreq, HEATING, FAN, BEAN_ENTRANCE, BEAN_EXIT, TESTLED


class BootstrapSerial():
    def readline(self):
        return np.random.randint(180, 220)

    def write(self, value):
        pass


def serial_init():
    try:
        s = Serial("COM3")
    except:
        s = BootstrapSerial()

    return s


def get_measurements():
    while True:
        with datalock:
            v = float(serial_read())
            print(v)
            data['t'].append(np.round(time(), 1))
            data['temp'].append(v)
            data['beantemp'].append((v+1024))
        sleep(1.0/samplefreq)


def handle_tasks():
    while True:
        while not tasks.empty():
            task = tasks.get()
            if task[0] == HEATING:
                pass
            elif task[0] == FAN:
                pass
            elif task[0] == BEAN_ENTRANCE:
                pass
            elif task[0] == BEAN_EXIT:
                pass
            elif task[0] == TESTLED:
                serial_write_int(task[1])

        sleep(1.0/samplefreq)



def serial_read():
    seriallock.acquire()
    value = ser.readline()
    seriallock.release()
    return value


def serial_write(value):
    seriallock.acquire()
    ser.write(value)
    seriallock.release()


def serial_write_int(value):
    serial_write(pack('>B', value))


data = defaultdict(partial(deque, maxlen=max_recorded))
tasks = Queue()
datalock = Lock()
seriallock = Lock()
ser = serial_init()

Thread(target=get_measurements).start()
Thread(target=handle_tasks).start()


