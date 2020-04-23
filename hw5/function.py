from typing import List
import logging
from itertools import combinations
from math import prod

def func(ar: List[int]) -> list:
    logger = logging.getLogger("main.function.func")
    assert type(ar) == list
    logger.error("input type assert")
    assert len(ar) > 0
    logger.error('Non empty list assert')
    assert all([isinstance(i, int) or isinstance(i, float) for i in ar])
    logger.error("Contains from floats or integer assert")
    logger.info(f"Compute new_ar from {ar}")
    new_ar = [prod(m) for m in combinations(ar[::-1], len(ar) - 1)]
    logger.info(f'Complete computations, new_ar: {new_ar}')
    return new_ar

# def func1(ar: List[int]) -> list:
#     new_ar = []
#     for i in ar:
#         prod = 1.0
#         a = ar.copy()
#         a.remove(i)
#         for j in a:
#             prod *= j
#         new_ar.append(prod)
#     return new_ar
