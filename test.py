import numpy as np
np_board = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
test_row = np.zeros((1, 10))
positions = np.arange(7)[:, np.newaxis] + np.arange(4)
test_row[0, positions] = [2, 32, 32, 4]
print(test_row)
matching_indices = np.where(np.all(np_board[0][positions] == test_row, axis=1))[0]
print(matching_indices)

