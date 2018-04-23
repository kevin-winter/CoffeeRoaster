import numpy as np
from struct import pack
from collections import defaultdict, deque
from queue import Queue
from functools import partial
from serial import Serial
from time import sleep, time
from threading import Thread, Lock
from defaults import max_recorded, samplefreq, HEATING, FAN, BEAN_ENTRANCE, BEAN_EXIT, TESTLED

data = defaultdict(partial(deque, maxlen=max_recorded))
tasks = Queue()
datalock = Lock()
seriallock = Lock()
ser = Serial("COM3")


def get_measurements():
    while True:
        with datalock:
            data['t'].append(np.round(time(), 1))
            data['temp'].append(int(serial_read()))
            data['beantemp'].append(np.random.randint(500))
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
                serial_write(pack('>B', task[1]))

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


Thread(target=get_measurements).start()
Thread(target=handle_tasks).start()
