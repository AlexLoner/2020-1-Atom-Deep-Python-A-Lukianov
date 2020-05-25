import numpy as np

def gen_board(size):
    mtx = np.random.randint(0, 2, size, dtype=np.int8)
    np.savetxt('data/theater/test.txt', mtx, fmt='%i', delimiter=' ')
