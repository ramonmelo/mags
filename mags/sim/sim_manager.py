
from dronekit_sitl import SITL
from subprocess import Popen

import time
import random
from shapely.geometry import Point, LineString, Polygon

import sys

class SimManager(object):

    def __init__(self):
        self.id = 0
        self.process_list = []

        # Bounding coordinations
        #           LAT          LON
        p1 = Point(-35.3617353, 149.1628940)
        p2 = Point(-35.3617410, 149.1661372)
        p3 = Point(-35.3643686, 149.1661373)
        p4 = Point(-35.3643801, 149.1629082)
        line = LineString([p1,p2,p3,p4])
        poly = Polygon(line)

        self.bound = poly
        self.lat_bound = poly.bounds[0], poly.bounds[2]
        self.lon_bound = poly.bounds[1], poly.bounds[3]

    def kill_all(self):
        for proc in self.process_list:
            proc.kill()

    def loop(self):
        print "loop init"

        while True:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                break
            finally:
                self.kill_all()

    def create_drone(self, lat, lon, idx):
        home_arg = '--home=%f,%f,584,353' % (lat, lon)
        instance_arg = '--instance %d' % idx
        path = '~/.dronekit/sitl/copter-3.3/apm' or 'copter'
        # , "--gimbal"

        print "Create drone with home at: ", (lat, lon)

        cmd = " ".join(['dronekit-sitl', path, home_arg, instance_arg])

        process = Popen(cmd, shell=True)
        self.process_list.append(process)

    def create_gcs(self, idx):
        base_port = 5760 + (10 * idx)
        base_url = "--master=tcp:127.0.0.1:%d" % base_port
        base_source = "--source-system=%d" % (200 + idx)

        cmd = " ".join(["mavproxy.py", base_url, "--map", "--console", base_source])

        process = Popen(cmd, shell=True)
        self.process_list.append(process)

    def create_system(self, **kwargs):
        if "lat" not in kwargs or "lon" not in kwargs:
            kwargs = self._create_random_position()

        kwargs["idx"] = self.id

        print "Create SITL Drone"
        self.create_drone(**kwargs)
        time.sleep(3)
        print "Create mavproxy"
        self.create_gcs(self.id)

        self.id += 1

        return True

    def _create_random_position(self):
        pos = None

        while True:
            pos = Point(random.uniform(*self.lat_bound), random.uniform(*self.lon_bound))
            if self.bound.contains(pos):
                break

        return {
            'lat': pos.x,
            'lon': pos.y
        }

if __name__ == "__main__":

    total = 1
    if len(sys.argv) > 1:
        total = int(sys.argv[1])

    manager = SimManager()

    for i in xrange(total):
        manager.create_system()

    manager.loop()
