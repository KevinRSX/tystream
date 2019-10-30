# this program plots the reward in time series
import sys
import numpy as np
import matplotlib.pyplot as plt

usage = "python3 plot_time_qoe.py [path_to_file]"
if len(sys.argv) != 2:
    sys.exit(usage)

path_to_file = sys.argv[1]
wall_time = []
rewards = []

with open(path_to_file, 'r') as f:
    calc_base = True
    base = 0.0
    for line in f:
        row = line.split()
        if calc_base:
            base = float(row[0])
            calc_base = False
        else:
            wall_time.append(float(row[0]) - base)
            rewards.append(cur_reward)
        cur_reward = float(row[6])


plt.scatter(wall_time, rewards)
plt.xlabel('time(s)')
plt.ylabel('reward')
plt.show()
