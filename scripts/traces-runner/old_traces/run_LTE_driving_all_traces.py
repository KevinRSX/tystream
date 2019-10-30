import os
import time
import json
import urllib
import subprocess

TRACE_PATH = '../cooked_traces/' 

with open('./chrome_retry_log', 'wb') as f:
	f.write('chrome retry log\n')

os.system('sudo sysctl -w net.ipv4.ip_forward=1')

ip_data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
ip = str(ip_data['ip'])

ABR_ALGO = 'fastMPC'
PROCESS_ID = 5
command_fastMPC = 'python run_LTE_driving_trace.py ' + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

proc_fastMPC = subprocess.Popen(command_fastMPC, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)

proc_fastMPC.wait()
