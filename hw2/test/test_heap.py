from max_heap import MaxHeap

my_heap = MaxHeap()
my_heap.heapify([8, 1, 5, 99, -12, 87])
print(f'my_heap init:  {my_heap.heap}')

my_heap.push(200)
print(f'my_heap push:  {my_heap.heap}')

pop_element = my_heap.pop()
print(f'my_heap pop:  {my_heap.heap}, {pop_element}')

my_heap.heapify([1, 2, 3, 4, 5, 6, 7])
print(f'my_heap redefine:  {my_heap.heap}')
