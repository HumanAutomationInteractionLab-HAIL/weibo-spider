import multiprocessing as mul


def f(n, a):
    n.value = 3.333
    a[0] = 4


if __name__ == "__main__":
    n = mul.Value('d', 0.00)
    a = mul.Array("i", range(10))
    print(n.value, a[0])
    process = mul.Process(target=f, args=(n, a))
    process.start()
    process.join()
    print(n.value, a[0])
    
