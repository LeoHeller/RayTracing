import multiprocessing as mp
import time

import math


def f(x):
    l = []
    for i in range(x):
        l.append(math.sqrt(x**x/x**x))
    return math.sqrt(math.sqrt(x ** 4))


if __name__ == "__main__":
    start = time.time()
    with mp.Pool(4) as pool:
        print(list(pool.imap_unordered(f, range(1000))))
        #print(pool.map(f, range(1000)))
    #print([f(x) for x in range(1000)])
    end = time.time()
    print(end - start)
