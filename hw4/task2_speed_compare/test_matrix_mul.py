import sys
sys.path.append('/home/loner/Documents/atoms/deep_python/2020-1-Atom-Deep-Python-A-Lukianov/hw4/build/lib.linux-x86_64-3.8')
import ctypes
import time
import python_matmul
import numpy as np
from matrix import Matrix

lib = ctypes.CDLL('./mylib.so')
t1 = time.time()
lib.mtx()
t2 = time.time() - t1
print(f"C time: {t2}\n")

t1 = time.time()
python_matmul.mtx()
t2 = time.time() - t1
print(f"python time: {t2}\n")



t1 = time.time()
g = Matrix([[i + 1 for i in range(6)] for j in range(6)])
g = Matrix([[i + 1 for i in range(6)] for j in range(6)])
print(g @ g)
t2 = time.time() - t1
print(f"Matrix time: {t2}\n")

t1 = time.time()
g = np.array([[i + 1 for i in range(6)] for j in range(6)])
g1 = np.array([[i + 1 for i in range(6)] for j in range(6)])
print(g.dot(g1))
t2 = time.time() - t1
print(f"Numpy time: {t2}\n")
