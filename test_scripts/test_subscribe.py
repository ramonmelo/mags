
import os
import sys
sys.path.append(os.getcwd())

import time
from mags import comm

def listen(data):
    print(data)

comm.Subscriber('/drone/info', listen)
# comm.Subscriber('/drone/info2', listen)

# while True:
#     try:
#         time.sleep(1)
#         print('sleep')
#     except KeyboardInterrupt:
#         break

print('done')
