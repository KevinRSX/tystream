# converts trace from mahimahi fomat to simulation format
# original: x (represent a chance of sending an MTU)
# coverted: [time_stamp (sec), throughput (Mbit/sec)]

import sys

MS_IN_SEC = 1000.0
MTU_SIZE = 1500
BITS_IN_BYTE = 8
BITS_IN_MBIT = 1000000

usage = "python trace_converter.py [input_trace] [output_trace]"
if len(sys.argv) < 3:
    sys.exit("usage: " + usage)

input_trace = sys.argv[1]
output_trace = sys.argv[2]

with open(input_trace, "r") as it, open(output_trace, "w") as ot:
    curr_time = 0.0
    curr_bw = 0.0
    for line in it:
        timestamp = float(line.rstrip("\n")) / MS_IN_SEC
        curr_bw += MTU_SIZE
        if timestamp - curr_time > 0.5:
            delay = timestamp - curr_time
            curr_time = timestamp
            throughput = curr_bw * BITS_IN_BYTE / BITS_IN_MBIT / delay
            ot.write(str(curr_time) + '\t' + str(throughput) + '\n')
            curr_bw = 0
        