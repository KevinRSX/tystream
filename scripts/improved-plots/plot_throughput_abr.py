import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import math

usage = "python3 plot_throughput_abr.py MS_PER_BIN cc_type trace_name output_file"

if len(sys.argv) < 5:
    sys.exit(usage)
MS_PER_BIN = int(sys.argv[1])
cc_type = sys.argv[2]
trace_name = sys.argv[3]
output_file = sys.argv[4]
file_paths = []
file_paths.append("../../results/fastMPC/" + cc_type + "/" + trace_name + "/" + cc_type + "_" + trace_name)
file_paths.append("../../results/robustMPC/" + cc_type + "/" + trace_name + "/" + cc_type + "_" + trace_name)
file_paths.append("../../results/rl/" + cc_type + "/" + trace_name + "/" + cc_type + "_" + trace_name)
print(file_paths)
abr_types = ["fastMPC", "robustMPC", "RL"]

def ms_to_bin(ms):
    return int(ms / MS_PER_BIN)

def bin_to_seconds(bin):
    return bin * MS_PER_BIN / 1000

durations = {}

def read_info(fp, abr_type):
    """
    Plot throughput-time graph for a file.
    Args:
        fp(str): file path to mahimahi data
        cc_type(str): congestion control type, for legend label
    """
    MIN_UNUSED_PREDICTION = 10000
    MAX_UNUSED_CAP = 2000
    all_capacity = {}
    all_departure = {}
    least_time = math.inf
    for i in range(1, 11):
        base_timestamp = None
        last_departure = MIN_UNUSED_PREDICTION
        with open(fp + str(i), 'r') as f:
            for line in f:
                row = str.split(line)
                # ignore heading lines
                if row[0] == '#':
                    continue
                timestamp = float(row[0])

                event_type = row[1]
                num_bytes = int(row[2])
                if len(row) > 3:
                    delay = row[3]

                num_bits = num_bytes * 8
                bin = ms_to_bin(timestamp)
                if base_timestamp == None:
                    base_timestamp = timestamp

                # three cases: capacity, arrival, departure, while
                # only capacity and departure are dealt with here
                # a chance to send
                if event_type == '#':
                    if bin in all_capacity:
                        all_capacity[bin] += num_bits
                    else:
                        all_capacity[bin] = num_bits
                # arrival, ignored
                elif event_type == '+':
                    continue
                # departure
                elif event_type == '-':
                    if bin in all_departure:
                        all_departure[bin] += num_bits
                    else:
                        all_departure[bin] = num_bits
                    if timestamp >= MIN_UNUSED_PREDICTION:
                        if last_departure == MIN_UNUSED_PREDICTION or timestamp - last_departure <= MAX_UNUSED_CAP:
                            last_departure = timestamp
                        elif timestamp - last_departure > MAX_UNUSED_CAP:
                            least_time = min(least_time, timestamp - base_timestamp)
                            break

    cap = []
    dep = []
    t = list(all_capacity.keys())
    t = sorted(x for x in t if x <= ms_to_bin(least_time))
    for key in t:
        cap.append(all_capacity[key])
        if key in all_departure:
            dep.append(all_departure[key])
        else:
            dep.append(0)
    t = [bin_to_seconds(x) for x in t]
    durations[cc_type] = t[-1] - t[0]

    cap = [x / 1000000 / 10 for x in cap]
    dep = [x / 1000000 / 10 for x in dep]
    plt.plot(t, dep, label=abr_type)
    return t, cap, durations[cc_type], sum(dep) / durations[cc_type]


ts = []
caps = []
ls = []
with open(output_file, 'w') as of:
    for i in range(len(abr_types)):
        t, cap, duration, mean_throughput = read_info(file_paths[i], abr_types[i])
        mean_capacity = sum(cap) / duration
        utilization = mean_throughput / mean_capacity * 100
        of.write("For " + abr_types[i] + "\n")
        of.write("Duration: " + f'{duration:.2f}' + "s\n")
        of.write("Mean throughput: " + f'{mean_throughput:.2f}' + "Mbits/s\n")
        of.write("Mean capacity: " + f'{mean_capacity:.2f}' + "Mbits/s\n")
        of.write("Utilization: " + f'{utilization:.2f}' + "%\n")
        of.write("\n")
        ts.append(t)
        caps.append(cap)
        ls.append(duration)

# plot maximum capacity
x = ls.index(max(ls))
plt.fill_between(ts[x], caps[x], 0, facecolor='pink', color='pink', alpha=0.2, label='capacity')

plt.xlabel("time(s)")
plt.ylabel("throughput(Mbits/s)")
plt.legend(loc='upper left')
plt.show()
