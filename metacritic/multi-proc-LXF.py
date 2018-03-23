import os, time, random
import multiprocessing as mul


def long_time_task(name):
    print("Run task %s (%s)..." % (name, os.getpid()))
    start = time.time()
    time.sleep(3)
    end = time.time()
    print("task %s runs %0.2f seconds" % (name, (end - start)))


if __name__ == '__main__':
    print("parent process %s" % os.getpid())
    pool = mul.Pool(4)
    for i in range(10):
        pool.apply_async(long_time_task, args=(i, ))
    print("waiting for all subpro")
    pool.close()
    pool.join()
    print("done")