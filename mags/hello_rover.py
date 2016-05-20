
from droid import Droid, DroidManager, Modes
from mission import Mission
import time

# try:

vehicle = DroidManager.connect_drone('tcp:127.0.0.1:5762', source_system = 200)

# vehicle.mission = Mission()

# vehicle.arm()
# vehicle.takeoff(15)

# vehicle.goto(-35.3620367, 149.1631986, speed = 15, altitude = 20)

# time.sleep(10)
# vehicle.gohome()

print vehicle.state()

time.sleep(4)
# vehicle.land()

vehicle.close()

#     while True:
#         print "Mode: %s" % vehicle.mode.name
#         time.sleep(1)
# except KeyboardInterrupt:
#     if vehicle:
#         vehicle.close()
