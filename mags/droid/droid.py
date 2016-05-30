
from dronekit import Vehicle, VehicleMode, LocationGlobal, LocationGlobalRelative
import time
import multiprocessing

from mags import comm
from mags.utils import Log

class Modes(object):
    auto   = 'AUTO'
    guided = 'GUIDED'
    rtl    = 'RTL'
    land   = 'LAND'

class Droid(Vehicle):

    # Droid Behaviors:
    # arm
    # disarm
    # takeoff
    # land
    # goto
    # status
    # state
    # execute_mission
    # gohome
    # altitude

    def __init__(self, *args):
        super(Droid, self).__init__(*args)
        self._mission = None

        self.id = None
        self.data = {}

        self.sub_info = comm.Subscriber('/drone/info', self.handler_info)
        self.pub_info = comm.Publisher('/drone/info')

    def run(self):
        while True:
            try:
                self.think()
            except KeyboardInterrupt:
                break
            finally:
                self.end()

    def think(self):
        time.sleep(1)
        self.pub_info.send( self.state() )

    def end(self):
        self.sub_info.end()

    # HANDLERS

    def handler_info(self, data):
        if data['id'] is not self.id:
            self.data[ data['id'] ] = data

    # COMMANDS

    def arm(self):
        while not self.is_armable:
            Log.i("Waiting initialization ...")
            time.sleep(1)

        Log.w("Arming motors")
        self.change_mode(Modes.guided)
        self.armed   = True

        while not self.armed:
            Log.w("Waiting for arming...")
            time.sleep(1)

    def disarm(self):
        self.armed = False

        while self.armed:
            Log.w("Waiting for disarming...")
            time.sleep(1)

    def takeoff(self, alt = 10):
        Log.i("Taking off!")
        self.simple_takeoff(alt)

        while True:
            if not self.in_guided():
                Log.e("User changed mode")
                break

            Log.d("ALT:", self.altitude())

            if self.altitude() >= (alt * 0.95):
                Log.i("Reached target altitude")
                break

            time.sleep(1)

    def land(self):
        self.change_mode(Modes.land)

    def goto(self, lat, lon, speed = 5, altitude = None):
        destination = LocationGlobalRelative(lat, lon, altitude or self.altitude())
        return self._goto(destination, speed)

    def goto_global(self, lat, lon, speed = 5, altitude = None):
        destination = LocationGlobal(lat, lon, altitude or self.altitude_global())
        return self._goto(destination, speed)

    def _goto(self, destination, speed):
        if not self.in_guided():
            return False

        dest_type = ""
        dest_type = "GLOBAL" if type(destination) is LocationGlobal else dest_type
        dest_type = "RELATIVE" if type(destination) is LocationGlobalRelative else dest_type

        dest_text = "(%s) LAT: %f \t LON: %f \t ALT: %f" % ( dest_type, destination.lat, destination.lon, destination.alt )

        Log.d("Going to: ", dest_text)
        self.simple_goto(destination, speed, speed)

        return True

    def gohome(self):
        self.change_mode(Modes.rtl)

    # UTILS

    def change_mode(self, mode):
        Log.i("Changing mode to:", mode)

        try:
            self.mode = VehicleMode(mode)
        except Exception, e:
            Log.e("Unknown mode:", mode)

    def in_guided(self):
        if self.mode.name is not Modes.guided:
            Log.e("Drone not in GUIDED mode")
            return False

        return True

    # MISSION RELATED

    @property
    def mission(self):
        return self._mission

    @mission.setter
    def mission(self, value):
        self._mission = value

    # STATE
    def state(self):
        battery = self.battery
        pos_global = self.location.global_frame
        pos_relative = self.location.global_relative_frame
        attitude = self.attitude

        return {
            'id': self.id,
            'position': {
                'alt': pos_global.alt,
                'alt_rel': pos_relative.alt,
                'lon': pos_global.lon,
                'lat': pos_global.lat
            },
            'ground_speed': self.groundspeed,
            'air_speed': self.airspeed,
            'battery': {
                'level': battery.level,
                'voltage': battery.voltage
            },
            'attitude': {
                'pitch': attitude.pitch,
                'roll': attitude.roll,
                'yaw': attitude.yaw
            },
            'heading': self.heading,
            'armable': self.is_armable,
            'armed': self.armed,
            'mode': self.mode.name
        }

    def altitude(self):
        return self.location.global_relative_frame.alt

    def altitude_global(self):
        return self.location.global_frame.alt

    # def status(self):
    #     # self is an instance of the self class
    #     print "Autopilot Firmware version: %s" % self.version
    #     print "Autopilot capabilities (supports ftp): %s" % self.capabilities.ftp
    #     print "Global Location: %s" % self.location.global_frame
    #     print "Global Location (relative altitude): %s" % self.location.global_relative_frame
    #     print "Local Location: %s" % self.location.local_frame    #NED
    #     print "Attitude: %s" % self.attitude
    #     print "Velocity: %s" % self.velocity
    #     print "GPS: %s" % self.gps_0
    #     print "Groundspeed: %s" % self.groundspeed
    #     print "Airspeed: %s" % self.airspeed
    #     print "Gimbal status: %s" % self.gimbal
    #     print "Battery: %s" % self.battery
    #     print "EKF OK?: %s" % self.ekf_ok
    #     print "Last Heartbeat: %s" % self.last_heartbeat
    #     print "Rangefinder: %s" % self.rangefinder
    #     print "Rangefinder distance: %s" % self.rangefinder.distance
    #     print "Rangefinder voltage: %s" % self.rangefinder.voltage
    #     print "Heading: %s" % self.heading
    #     print "Is Armable?: %s" % self.is_armable
    #     print "System status: %s" % self.system_status.state
    #     print "Mode: %s" % self.mode.name    # settable
    #     print "Armed: %s" % self.armed    # settable

    # def attitude_callback(self, self, attr_name, value):
        # pass

    # def gps_callback(self, self, attr_name, value):
        # pass
