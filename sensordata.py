import numpy as np
from collections import defaultdict, deque
from functools import partial
from serial import Serial
from time import sleep, time
from threading import Thread, Lock

freq = 2 #Hz
max_recorded = int(10*60*freq)
data = defaultdict(partial(deque, maxlen=max_recorded))
datalock = Lock()

def get_measurements():
    with Serial("COM3") as ser:
        while True:
            with datalock:
                data['t'].append(np.round(time(), 1))
                data['temp'].append(int(ser.readline()))
            sleep(1.0/freq)

Thread(target=get_measurements).start()
