import sys
import os
import subprocess
import numpy as np


RUN_SCRIPT = 'run_video.py'
RANDOM_SEED = 42
RUN_TIME = 100  # sec
MM_DELAY = 40   # millisec


def main():
	trace_path = sys.argv[1]
	abr_algo = sys.argv[2]
	process_id = sys.argv[3]
	ip = sys.argv[4]
	trace_name = sys.argv[5]
	result_name = sys.argv[6]

	sleep_vec = range(1, 10)  # random sleep second

	# files = os.listdir(trace_path)
	# for f in files:
	f1 = 'Verizon-LTE-short.up'
	# f2 = 'Verizon-LTE-short.down'

	for k in range(1, 11):
		while True:
			np.random.shuffle(sleep_vec)
			sleep_time = sleep_vec[int(process_id)]

			proc = subprocess.Popen('mm-delay ' + str(MM_DELAY) + ' mm-link --uplink-log=./results/uplink' + str(k) + ' --downlink-log=./results/' + result_name + str(k) + ' ' + trace_path + f1 + ' ' + trace_path + trace_name + ' /usr/bin/python ' + RUN_SCRIPT + ' ' + ip + ' ' + abr_algo + ' ' + str(RUN_TIME) + ' ' + process_id + ' ' + trace_name  + ' ' + str(sleep_time) + ' ' + str(k), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()

			if out == 'done\n':
				break
			else:
				with open('./chrome_retry_log', 'ab') as log:
					log.write(abr_algo + '_' + f + '\n')
					log.write(out + '\n')
					log.flush()



if __name__ == '__main__':
	main()
