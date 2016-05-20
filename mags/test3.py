import multiprocessing
import time

class Worker(multiprocessing.Process):

    def __init__(self, time):
        super(Worker, self).__init__()
        self.time = time

    def run(self):
        print("okey", self.time)
        time.sleep(self.time)
        print("done")

if __name__ == '__main__':
    w1 = Worker(1)
    w2 = Worker(2)

    w1.start()
    w2.start()

    w1.join()
    w2.join()
