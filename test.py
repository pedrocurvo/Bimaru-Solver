import numpy as np
import time

# Example array
arr = np.array([[2, 0, 0, 0, 2, 0, 2, 3], [2, 3, 0, 5, 8, 9, 7, 6]])

# Count the occurrences of a specific element
empty = np.count_nonzero(arr[1] == 0)
print(np.array_equal(arr[0][0:3],  [2, 0, 0]) ) # Output: 4
arr[0][0:3] = [1, 1, 1]
print(arr)




