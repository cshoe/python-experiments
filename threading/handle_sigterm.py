import functools
import signal
import threading
import time


class WorkerThread(threading.Thread):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self.should_stop = threading.Event()

    def run(self):
        iteration = 0
        while True:
            time.sleep(2)
            if self.should_stop.isSet():
                return
            print 'Doing woooooork {}'.format(iteration)
            iteration += 1


def sigterm_handler(signal_number, stack_frame, thread=None):
    print 'Handling SIGTERM'
    thread.should_stop.set()
    thread.join(10)


def main():
    thread = WorkerThread()
    handler_function = functools.partial(sigterm_handler, thread=thread)
    signal.signal(signal.SIGTERM, handler_function)
    thread.start()


if __name__ == '__main__':
    main()
