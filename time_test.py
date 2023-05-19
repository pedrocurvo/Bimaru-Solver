import time
import os
media = []
for i in range(1, 11):
    #if i == 10: continue
    start_time = time.time()
    os.system(f'python3 bimaru2.py < Instances/instance{i:02d}.txt')
    end_time = time.time()
    print(f'----- Instance {i} -----')
    print("--- %s seconds ---" % (end_time - start_time))
    media.append(end_time - start_time)

print(f'Media: {sum(media)/len(media)}')