import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import math

file_paths = [sys.argv[1], sys.argv[2]]
output_file = sys.argv[3]
congestion_control_types = ['CUBIC', 'BBR']

durations = {}

def read_info(fp, cc_type):
    MIN_UNUSED_PREDICTION = 10000
    MAX_UNUSED_CAP = 2000
    delays = []
    signal_delay = [{} for i in range(11)]
    least_time = math.inf
    for i in range(1, 11):
        signal_delay[i] = {}
        base_timestamp = None
        last_departure = MIN_UNUSED_PREDICTION
        with open(fp + str(i), 'r') as f:
            for line in f:
                row = str.split(line)
                # ignore heading lines
                if row[0] == '#':
                    continue
                timestamp = int(row[0])

                event_type = row[1]
                num_bytes = int(row[2])
                if len(row) > 3:
                    delay = int(row[3])

                if base_timestamp == None:
                    base_timestamp = timestamp

                # only consider departure, where the delay is measured
                if event_type == '#':
                    continue
                elif event_type == '+':
                    continue
                elif event_type == '-':
                    if timestamp - delay in signal_delay[i]:
                        signal_delay[i][timestamp - delay] = min(delay, signal_delay[i][timestamp - delay])
                    else:
                        signal_delay[i][timestamp - delay] = delay
                    delays.append(delay)
                    if timestamp >= MIN_UNUSED_PREDICTION:
                        if last_departure == MIN_UNUSED_PREDICTION or timestamp - last_departure <= MAX_UNUSED_CAP:
                            last_departure = timestamp
                        elif timestamp - last_departure > MAX_UNUSED_CAP:
                            least_time = min(least_time, timestamp - base_timestamp)
                            break

    average_signal_delay = {}
    # calculate average singal_delay -- timestamp: delay in ms
    for i in reversed(range(int(least_time))):
        average_signal_delay[i] = 0
        for j in range(1, 11):
            if i in signal_delay[j]:
                # print(average_signal_delay[i])
                average_signal_delay[i] += signal_delay[j][i]
        average_signal_delay[i] /= 10
        if average_signal_delay[i] == 0 and i < least_time - 1:
            average_signal_delay[i] = average_signal_delay[i + 1]

    t = list(average_signal_delay.keys())
    t.sort()
    signal_delay_points = [average_signal_delay[x] for x in t]
    t = [x / 1000 for x in t]
    plt.plot(t, signal_delay_points, label=cc_type)
    return signal_delay_points


# calculate statistics and plot different files
with open(output_file, 'w') as of:
    for i in range(2):
        signal_delays = read_info(file_paths[i], congestion_control_types[i])
        of.write("For " + congestion_control_types[i] + ":\n")
        signal_delays.sort()
        pp90 = signal_delays[int(0.9 * len(signal_delays))]
        pp95 = signal_delays[int(0.95 * len(signal_delays))]
        pp99 = signal_delays[int(0.99 * len(signal_delays))]
        of.write("90 percentile delay: " + str(pp90) + "ms\n")
        of.write("95 percentile delay: " + str(pp95) + "ms\n")
        of.write("99 percentile delay: " + str(pp99) + "ms\n")
        of.write("\n")


plt.xlabel("time(s)")
plt.ylabel("delay(ms)")
plt.legend(loc='upper left')
plt.show()
