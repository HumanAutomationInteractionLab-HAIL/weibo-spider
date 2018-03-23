import threading
import time
import os


def doChore():
    time.sleep(0.1)


class BoothThreading(threading.Thread):
    def __init__(self, count, monitor):
        self.count = count
        self.monitor = monitor
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.monitor['lock'].acquire()
            if self.monitor["tick"] != 0:
                self.monitor["tick"] = monitor["tick"] - 1
                print(self.count, "left", self.monitor["tick"])
                doChore()
            else:
                print("no tickets left")
                os._exit(0)
            self.monitor["lock"].release()


#start main
monitor = {"tick": 10, "lock": threading.Lock()}

#start 10 threads

workers = []
for k in range(10):
    new_thread = BoothThreading(k, monitor)
    workers += [new_thread]
    print("meanless")
    new_thread.start()
    #new_thread.join()

for worker in workers:
    worker.close()
    worker.join()