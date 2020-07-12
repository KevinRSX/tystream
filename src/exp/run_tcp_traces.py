import sys
import os
import subprocess
import time
import argparse

from emulator import Emulator # only called when dir is in exp/

# usage = "python run_quic_traces.py [trace_name] [log_name] [running_time]"
parser = argparse.ArgumentParser()
parser.add_argument("trace_name")
parser.add_argument("log_name")
parser.add_argument("run_times")
args = parser.parse_args()
trace_name = args.trace_name
trace_path = "./cooked_traces/" + args.trace_name
log_name = args.log_name
run_times = int(args.run_times)

#log name: trace + transport + cc + abr
abr = log_name.split('_')[-1]
cc = log_name.split('_')[-2]


for id in range(1, run_times + 1):
    print("****************************************************************************************************")
    print("Running test number " + str(id))
    print("****************************************************************************************************")

    emulator = Emulator(trace_name, log_name)
    cmd_mm = emulator.generate_emulation_cmd(id)
    print(cmd_mm)

    proc = subprocess.Popen(cmd_mm + ' ' + "python run_tcp_video.py " + abr + " " + cc + " tcp " + trace_name + " " + str(id), shell=True)
    proc.wait()
    time.sleep(1)