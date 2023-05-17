import time
import os
for i in range(1, 11):
    start_time = time.time()
    os.system(f'python3 bimaru.py < Instances/instance{i:02d}.txt')
    end_time = time.time()
    print(f'----- Instance {i} -----')
    print("--- %s seconds ---" % (end_time - start_time))