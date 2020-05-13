import log_reader.mahimahi as mm
import log_reader.rl_server as rl
import numpy as np
import matplotlib.pyplot as plt
import os

all_abr = ["fastMPC", "robustMPC", "rl"]
plot_cap = True

for abr in all_abr:
    bw_dict = {}
    rl_times = np.zeros(14)
    rl_estimations = np.zeros(14)
    for i in range(1, 11): # read mahimahi and rl logs
        mm_path = "../../results/quic/" + abr + "/" + "qcubic_att_driving_down" + str(i)
        rl_path = "../../results/quic/" + abr + "/" + "log_" + abr + "_qcubic_ATT-LTE-driving" + str(i)
        print(rl_path)
        mahimahi_reader = mm.MMReader(mm_path, 1000, 60000)
        for key, value in mahimahi_reader.all_capacity.items():
            if key in bw_dict.keys():
                bw_dict[key] += value
            else:
                bw_dict[key] = value
        
        rl_reader = rl.RLReader(rl_path)
        times = rl_reader.relative_timestamps(mahimahi_reader.initial_time)
        
        estimations = rl_reader.estimations
        rl_times = np.add(rl_times, times)
        rl_estimations = np.add(rl_estimations, estimations)

    if plot_cap == True:
        times, caps = mm.MMReader.get_lists_from_dict(bw_dict, 1000)
        caps = [x / 10 for x in caps]
        plt.fill_between(times, caps, 0, facecolor='pink', color='pink', alpha=0.3, label='capacity')
        plot_cap = False

    rl_times = [x / 10 for x in rl_times]
    rl_estimations = [x / 10 for x in rl_estimations]
    plt.plot(rl_times, rl_estimations, label=abr)

    
plt.xlabel("time(s)")
plt.ylabel("throughput(Mbits/s)")
plt.legend(loc='upper right')
plt.show()
