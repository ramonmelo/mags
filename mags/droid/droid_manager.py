
import dronekit
from droid import Droid

from utils import Log

class DroidManager():

    @staticmethod
    def connect_drone(url, source_system = 255, baud = 115200):
        drone = None

        try:
            drone = dronekit.connect(
                ip                 = url,
                wait_ready         = True,
                heartbeat_timeout  = 15,
                baud               = baud,
                source_system      = source_system,
                vehicle_class      = Droid)

        # Bad TCP connection
        except socket.error:
            Log.e('No server exists!')

        # Bad TTY connection
        except exceptions.OSError as e:
            Log.e('No serial exists!')

        # API Error
        except dronekit.APIException:
            Log.e('Timeout!')

        # Other error
        except Exception as e:
            Log.e('Some other error:', e)

        return drone
