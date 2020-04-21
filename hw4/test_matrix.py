import sys
sys.path.append('/home/loner/Documents/atoms/deep_python/2020-1-Atom-Deep-Python-A-Lukianov/hw4/build/lib.linux-x86_64-3.8')

import numpy as np
from matrix import Matrix

g = Matrix([[1.0, -2],
            [3, 4],
            [-5, 6.5]])

h = Matrix([[-10.0, 2],
            [3, -4],
            [5, 6.5]])

print('Init mtx ')
print(f'g \n{g}')
print(f'h \n{h}')

print(f'Get number g[(2,1)] = {g[(2,1)]}')
print(f"g.__repr__() \n {g.__repr__()}")


print('Adding matrices t1 = g + h')
t1 = g + h
print(f't1 \n {t1}')
print(f'g \n{g}')
print(f'h \n{h}')

print('Subtract matrices t2 = g - h')
t2 = g - h
print(f't2 \n {t2}')
print(f'g \n{g}')
print(f'h \n{h}')

print('Multiplication matrix by number t3 = g * 2.5')
t3 = g * 2.5
print(f't3 \n {t3}')
print(f'g \n{g}')

print('Multiplication matrix by number t4 = 2.5 * g')
t4 = 2.5 * g
print(f't4 \n {t4}')
print(f'g \n{g}')

print('True_divide matrix by number t5 = g / 2.5')
t5 = g / 2.5
print(f't5 \n {t5}')
print(f'g \n{g}')

print('Transpose g matrix')
print(g.transpose())

g = g.transpose()
print('__matmul__ g @ h')
print(g @ h)
g1 = np.array(g.dense)
h1 = np.array(h.dense)
print('numpy __matmul__')
print(g1 @ h1)




