import sys
sys.path.append('/home/loner/Documents/atoms/deep_python/2020-1-Atom-Deep-Python-A-Lukianov/hw4/build/lib.linux-x86_64-3.8')
from matrix import Matrix

g = Matrix([[1.0, 2],
            [3, 4],
            [5, 6.5]])
print(g.dense)

print(g.__repr__())
for i in range(g.shape[0]):
    for j in range(g.shape[1]):
        print(g[(i, j)], end=" ")

print()

print(g[(6,0)])



