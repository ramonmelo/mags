
import zmq
import pickle

def run():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:7002")
    socket.setsockopt_string(zmq.SUBSCRIBE, u'')

    print "Echo data"

    while True:
        msg = socket.recv_multipart()
        topic, data = msg

        print( pickle.loads(data) )

if __name__ == "__main__":
    run()
