import bisect

class MedianFinder:

    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.data = []
        self.pointer = -0.5
    
    # ---------------------------------------------------------------------------------------------
    def addNum(self, num: int) -> None:
        bisect.insort_left(self.data, num)
        self.pointer += 0.5

    # ---------------------------------------------------------------------------------------------
    def findMedian(self) -> float:
        return self.data[int(self.pointer)] if self.pointer % 1 == 0.0 \
            else 0.5 * (self.data[int(self.pointer - 0.5)] + self.data[int(self.pointer + 0.5)])
