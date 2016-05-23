
import zmq
import time
import pickle

def run():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:7001")

    print "White data"

    data = {
        'name': 'robot 1',
        'value': 10
    }

    while True:
        info = pickle.dumps(data)

        socket.send_multipart([b'/droid/2/info', info])
        time.sleep(0.5)

if __name__ == '__main__':
    run()
