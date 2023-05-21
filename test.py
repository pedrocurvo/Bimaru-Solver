import numpy as np
import time
np_array = np.array([1, 2, 3, 4,5, 0, 7, 0, 8, 9, 10])

start_time = time.time()
coordinates = [i for i in range(len(np_array)) if np_array[i] == 0]
end_time = time.time()
print(f"--- {end_time - start_time} seconds ---")
start_time = time.time()
coordinates = np.where(np_array == 0)[0]
end_time = time.time()
print(f"--- {end_time - start_time} seconds ---")



