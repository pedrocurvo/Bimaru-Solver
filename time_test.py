import time
import os
media = []
for i in range(1, 31):
    #if i == 10: continue
    start_time = time.time()
    os.system(f'python3 bimaru.py < Instances/instance{i:02d}.txt')
    end_time = time.time()
    print(f'----- Instance {i} -----')
    print(f"--- {end_time - start_time} seconds ---")
    media.append(end_time - start_time)

print(f'Media: {sum(media)/len(media)}')