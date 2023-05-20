import numpy as np

# Example arrays
larger_array = np.array([0, 8, 32, 32, 16, 0, 0, 0, 0, 0])
smaller_array = np.array([8, 32, 32, 16])

for a in range(len(larger_array) - len(smaller_array) + 1):
    if np.array_equal(larger_array[a:a + len(smaller_array)], smaller_array):
        contains_smaller_array = True
        break
    else:
        contains_smaller_array = False

print(contains_smaller_array)  # Output: True


col_compare = np.array([0, 8, 32, 32, 17, 0, 0, 0, 0, 0])
row_compare = np.array([8, 32, 32, 16])
col_number = np.array([0, 8, 32, 32, 16, 0, 0, 0, 0, 0])
row_number = np.array([8, 32, 32, 16])

print(col_compare == col_number)
print(np.argwhere(col_compare == col_number))

matriz = np.array([[0, 8, 32, 32, 16, 0, 0, 0, 0, 0],
                   [0, 8, 32, 32, 16, 0, 0, 0, 0, 0]])
matriz[:,0] = np.where(matriz[:,0] == 0, 1, matriz[0])
print(matriz)