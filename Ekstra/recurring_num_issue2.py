from itertools import permutations 
import numpy as np
import collections

b = np.array([1, 5, 2, 4, 4, 7, 7, 9, 8])
a = np.array([2, 0, 2, 1, 2, 3])


print([item for item, count in collections.Counter(a).items() if count > 1])
