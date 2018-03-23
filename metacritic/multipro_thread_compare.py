# To print the PID of thread and process
# A comparison of using multiprocessing and multithread
import os
import multiprocessing
import threading
import time


def worker(sign, lock):
    print("what")

    lock.acquire()
    print(sign, os.getpid())
    doChore()
    lock.release()


def doChore():
    time.sleep(3)


# Main
print("Main:", os.getpid())

# Multi-thread
record = []
lock = threading.Lock()
for i in range(5):
    new_thread = threading.Thread(target=worker, args=("Threading", lock))
    new_thread.start()
    record.append(new_thread)
for i in range(5):
    record[i].join()

# Multi-process
#record = []
#lock = multiprocessing.Lock()
#for i in range(5):
#    new_process = multiprocessing.Process(
#        target=worker, args=("Process", lock))
#    new_process.start()
#    record.append(new_process)
#for process in record:
#    record[i].join()
