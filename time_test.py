import time
import os
media = []
for i in range(14, 15):
    if i == 10: continue
    start_time = time.time()
    os.system(f'python3 bimaru.py < Instances/instance{i:02d}.txt')
    end_time = time.time()
    print(f'----- Instance {i} -----')
    print("--- %s seconds ---" % (end_time - start_time))
    media.append(end_time - start_time)

print(f'Media: {sum(media)/len(media)}')