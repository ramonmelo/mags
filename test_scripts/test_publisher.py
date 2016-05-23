
import os
import sys
sys.path.append(os.getcwd())

import time
from mags import comm

pubs1 = comm.Publisher('/drone/info1')
pubs2 = comm.Publisher('/drone/info2')

data1 = {
    'name': 'robot 1',
    'value': 10
}

data2 = {
    'name': 'robot 2',
    'value': 10
}

while True:
    try:
        pubs1.send(data1)
        pubs2.send(data2)

        time.sleep(1)
    except KeyboardInterrupt:
        break
