import numpy as np
import time

# Example array
arr = np.array([2, 3, 2, 4, 2, 1, 2, 3])

# Count the occurrences of a specific element
arr = np.where(np.isin(arr, [2, 3]), 1, arr)
print(arr)  # Output: 4



