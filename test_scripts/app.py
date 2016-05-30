
import os
import sys
sys.path.append(os.getcwd())

from mags.droid import DroidManager

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 5760

if len(sys.argv) > 2:
    idx = int(sys.argv[2])
else:
    idx = 0

url = 'tcp:127.0.0.1:%d' % (port)

vehicle = DroidManager.connect_drone(url, idx, source_system = 200)
vehicle.run()
