
import pickle
import zmq

class Publisher(object):

    def __init__(self, topic):
        self.topic = topic

        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.connect("tcp://127.0.0.1:7001")

        self.socket = socket

    def send(self, data):
        info = pickle.dumps(data)
        self.socket.send_multipart([self.topic, info])


