
import pickle
import zmq
import multiprocessing

class Subscriber(object):

    def __init__(self, topic, callback):
        self.topic = unicode(topic)
        self.callback = callback
        self.socket = None

        self.process = multiprocessing.Process(target=self._run)
        self.process.start()

    def _run(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://127.0.0.1:7002")
        socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)

        self.socket = socket

        while True:
            msg = self.socket.recv_multipart()
            topic, data = msg

            self.callback(pickle.loads(data))

    def end(self):
        self.process.terminate()
