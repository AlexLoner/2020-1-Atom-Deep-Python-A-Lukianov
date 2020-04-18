from median import MedianFinder
import numpy as np

obj = MedianFinder()
for i in np.random.randint(-10, 10, 7):
    obj.addNum(i)
    median = obj.findMedian()
    print('#---------------------------------')
    print(f'Median :: {median}\nFull array :: {obj.data}\n')
