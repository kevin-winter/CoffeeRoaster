import numpy as np
from collections import defaultdict, deque
from queue import Queue
from functools import partial
from serial import Serial
from time import sleep, time
from threading import Thread, Lock

import defaults

data = defaultdict(partial(deque, maxlen=defaults.max_recorded))
tasks = Queue()
datalock = Lock()

def get_measurements():
    with Serial("COM3") as ser:
        while True:
            with datalock:
                data['t'].append(np.round(time(), 1))
                data['temp'].append(int(ser.readline()))
                data['beantemp'].append(np.random.randint(500))
            sleep(1.0/defaults.samplefreq)

Thread(target=get_measurements).start()
