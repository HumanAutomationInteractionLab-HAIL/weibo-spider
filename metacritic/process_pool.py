import multiprocessing as mul


def f(x, y):
    return x * y


if __name__ == "__main__":
    pool = mul.Pool(5)
    rel = pool.map(f, [x for x in range(100)])
    #rel = pool.apply_async(f, args=(100, 200))
    print(rel)
    pass