import numpy as np

array = np.array([[1, 2, 3, 4, 5, 6, 7], 
                 [1, 2, 3, 4, 5, 6, 7]])
values = [2, 4, 6, 7]

count_different = np.count_nonzero(~np.isin(array, values))

print(count_different)
