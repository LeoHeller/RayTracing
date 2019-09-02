import numpy as np
from timeit import default_timer as timer
from numba import vectorize, float64


@vectorize([float64(float64)])
def add_one(a):
    return a + 1


@vectorize([float64(float64, float64)], target='cuda')
def pow(a, b):
    # return add_one(a ** b)
    return a ** b


def main():
    vec_size = 100_000_000
    a = b = np.array(np.random.sample(vec_size), dtype=np.float64)
    c = np.zeros(vec_size, dtype=np.float64)

    start = timer()

    c = pow(a, b)
    duration = timer() - start

    print(duration)


if __name__ == "__main__":
    main()
