from task_3 import A

a = A(10, 'euro')
b = A(8, 'usd')
c = A(5)
d = A(1, 'gbp')

print(a + b)
print(b + a)
a1 = b + a
a1.send_to('euro')
print(a1)

print(a + c)
print(c + d)
print(c + c)