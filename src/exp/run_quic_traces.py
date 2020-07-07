import sys
import os
import subprocess
import time
from emulator import Emulator # only called when dir is in exp/

usage = "python run_quic_traces.py [trace_name] [log_name] [running_time]"
if len(sys.argv) < 4:
    sys.exit("usage: " + usage)
trace_name = sys.argv[1]
trace_path = "./cooked_traces/" + trace_name
log_name = sys.argv[2]
log_path = "./results/" + log_name
running_time = int(sys.argv[3])

for id in range(1, running_time + 1):
    print("****************************************************************************************************")
    print("Running test number " + str(id))
    print("****************************************************************************************************")

    emulator = Emulator(trace_name, log_name)
    cmd_mm = emulator.generate_emulation_cmd(id)
    print(cmd_mm)

    proc = subprocess.Popen(cmd_mm + ' ' + "python run_quic_video.py " + trace_name + str(id), shell=True)
    proc.wait()
    time.sleep(3)