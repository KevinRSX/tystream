import sys
import os
import numpy as np
import matplotlib.pyplot as plt
# usage:
# python3 plot_bitrate.py [path_to_file]

f_path = sys.argv[1]
wall_time = []
bitrate = []

with open(f_path, 'r') as f:
    calc_base = True
    base = 0.0
    for line in f:
        row = line.split()
        if calc_base:
            calc_base = False
            base = float(row[0])
        wall_time.append(float(row[0]) - base)
        bitrate.append(float(row[1]))

# adjust the list so that the bitrate corresponds with correct time
bitrate.insert(0, 0.0)
wall_time.insert(len(wall_time), wall_time[-1])
plt.step(wall_time, bitrate)
plt.xlabel('time(s)')
plt.ylabel('bitrate(kbps)')
plt.title('Bitrate - Time Graph')
plt.show()
