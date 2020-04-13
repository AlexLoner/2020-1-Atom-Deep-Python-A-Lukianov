from typing import List


class MaxHeap:

    # ---------------------------------------------------------------------------------------------
    def __init__(self) -> None:
        self.heap_len = 0
        self.heap = []

    # ---------------------------------------------------------------------------------------------
    def push(self, val: int) -> None:
        self.heap_len += 1
        self.heap.append(val)
        self.shift_up()

    # ---------------------------------------------------------------------------------------------
    def pop(self) -> int:
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        max_element = self.heap.pop()
        self.heap_len -= 1
        self.shift_down()
        return max_element

    # ---------------------------------------------------------------------------------------------
    def heapify(self, iterable: List[int]) -> None:
        self.heap.clear()
        self.heap_len = 0
        for item in iterable:
            self.push(item)

    # ---------------------------------------------------------------------------------------------
    def _calc_parent(self, number):
        return (number - 1) // 2

    # ---------------------------------------------------------------------------------------------
    def _calc_children(self, number):
        return 2 * number + 1, 2 * (number + 1)

    # ---------------------------------------------------------------------------------------------
    def shift_up(self):
        index = self.heap_len - 1
        while True:
            parent = self._calc_parent(index)
            if index > 0 and self.heap[index] > self.heap[parent]:
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                index = parent
            else:
                break

    # ---------------------------------------------------------------------------------------------
    def shift_down(self):
        index = 0
        while True:
            children = self._calc_children(index)
            if children[1] < self.heap_len:  # Значит сущ-ют оба ребенка
                candidates = [self.heap[children[0]], self.heap[children[1]]]
                element_to_swap = max(candidates)
                index_to_swap = index + self.heap[index:].index(element_to_swap)

                if self.heap[index_to_swap] > self.heap[index]:
                    self.heap[index_to_swap], self.heap[index] = self.heap[index], self.heap[index_to_swap]
                    index = index_to_swap

            elif children[0] < self.heap_len and self.heap[children[0]] > self.heap[index]:
                self.heap[children[0]], self.heap[index] = self.heap[index], self.heap[children[0]]
                index = children[0]
            else:
                break
