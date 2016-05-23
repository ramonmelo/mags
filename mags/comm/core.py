
import zmq
import multiprocessing
import time

def spin():
    process = multiprocessing.Process(target=run)
    process.start()

    while True:
        try:
            process.join()
        except KeyboardInterrupt:
            break
        finally:
            process.terminate()

def run():
    print("Init core server")
    context = zmq.Context()

    subscriber = context.socket(zmq.XSUB)
    publisher = context.socket(zmq.XPUB)

    subscriber.bind("tcp://127.0.0.1:7001")
    publisher.bind("tcp://127.0.0.1:7002")

    # IN, OUT
    zmq.proxy(subscriber, publisher)

if __name__ == "__main__":
    run()
