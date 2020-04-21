import sys
sys.path.append('/home/loner/Documents/atoms/deep_python/2020-1-Atom-Deep-Python-A-Lukianov/hw4/build/lib.linux-x86_64-3.8')
import ctypes
import time
import python_matmul

lib = ctypes.CDLL('./mylib.so')
t1 = time.time()
lib.mtx()
t2 = time.time() - t1
print(f"C time: {t2}")

t1 = time.time()
python_matmul.mtx()
t2 = time.time() - t1
print(f"python time: {t2}")
