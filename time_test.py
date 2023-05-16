import time
import os
for i in range(1, 10):
    start_time = time.time()
    os.system(f'python3 bimaru.py < instance0{i}.txt')
    end_time = time.time()
    print(f'----- Instance {i} -----')
    print("--- %s seconds ---" % (end_time - start_time))


