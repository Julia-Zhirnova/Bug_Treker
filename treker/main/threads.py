import threading
import queue
import sys
import json
import traceback
from .testing_worker import Tester


class Testing(threading.Thread):
    def __init__(self, e_queue, file_name):
        threading.Thread.__init__(self)
        self.err_queue = e_queue
        self.filename = file_name
        print("Initialized thread")

    def run(self):
        n_t = Tester(self.filename)
        n_t.syntax_test()
        com=n_t.compiling_()
        try:
            eval(com)
            print('no')
        except:
            trace=traceback.format_exc()
            n_t.runtime_test(trace)
        self.err_queue.put(n_t.report_items)


def main():
    err_queue = queue.Queue()
    worker = Testing(err_queue, 'erors_file.py')
    worker.setDaemon(False)
    worker.start()
    worker.join()
    while not err_queue.empty():
        print(err_queue.get())


if __name__ == '__main__':
    main()
