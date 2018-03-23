import multiprocessing as mul


def pro1(pipe):
    pipe.send("hello")
    print("pipe rec:", pipe.recv())


def pro2(pipe):
    print("pipe rec:", pipe.recv())
    pipe.send("hello too")


if __name__ == "__main__":
    # Build a pipe
    pipe = mul.Pipe()  #duplex=False)
    # Pass an end of pipe to Pro1
    p1 = mul.Process(target=pro1, args=(pipe[0], ))
    # Pass another end
    p2 = mul.Process(target=pro2, args=(pipe[1], ))
    p1.start()

    p2.start()
    p1.join()

    p2.join()
