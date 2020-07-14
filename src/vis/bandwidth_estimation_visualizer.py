from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

from vis.generic_visualizer import GenericVisualizer
import vis.log_reader.mahimahi as mm
import vis.log_reader.rl_server as rl
import exp.abr_name_converter as name_converter


class BandwidthEstimationVisualizer(GenericVisualizer):
    def __init__(self, config):
        GenericVisualizer.__init__(self, config)
        self.CHUNK_NUM = 48
        self.form_paths()
        self.process_data()
    
    def form_paths(self):
        self.mm_path = []
        self.mm_trace = 'Verizon-LTE-short'
        self.mm_transport = 'quic'
        self.mm_cc = 'cubic'
        for i in range(len(self.variants)):
            full_path = self.directories[i] + self.mm_trace + '_' + self.mm_transport + '_' + self.mm_cc + '_' + self.variants[i]
            self.mm_path.append(full_path)
        
        self.rl_path = []
        self.rl_trace = 'Verizon-LTE-short'
        self.rl_transport = 'quic'
        self.rl_cc = 'cubic'
        for i in range(len(self.variants)):
            full_path = self.directories[i] + "log_" + name_converter.to_html(self.variants[i]).split('_')[-1] + '_' + self.rl_transport + '_' + self.rl_cc + '_' + self.rl_trace
            self.rl_path.append(full_path)
    
    def process_data(self):
        self.bw_dict = []
        for prefix in self.mm_path:
            departure_dict = {}
            for i in range(1, 3):
                mahimahi_reader = mm.MMReader(prefix + str(i), 1000, 220000)
                for key, value in mahimahi_reader.all_departure.items():
                    if key in departure_dict.keys():
                        departure_dict[key] += value
                    else:
                        departure_dict[key] = value
            self.bw_dict.append(departure_dict)
        
        # assume same trace
        self.capacity_dict = {}
        mahimahi_reader = mm.MMReader(self.mm_path[0] + '1', 1000, 220000)
        for key, value in mahimahi_reader.all_capacity.items():
            if key in self.capacity_dict.keys():
                self.capacity_dict[key] += value
            else:
                self.capacity_dict[key] = value
        
        self.all_estimations = [] # [[[time], [est]], ...,]
        for i in range(2): # variant index
            self.all_estimations.append([])
            self.all_estimations[i].append(np.zeros(self.CHUNK_NUM))
            self.all_estimations[i].append(np.zeros(self.CHUNK_NUM))
            for j in range(1, 3): # exp runtime index
                rl_reader = rl.RLReader(self.rl_path[i] + str(j))
                mahimahi_reader = mm.MMReader(self.mm_path[i] + str(j), 1000, 220000)
                times = rl_reader.relative_timestamps(mahimahi_reader.initial_time)
                estimations = rl_reader.estimations

                self.all_estimations[i][0] = np.add(self.all_estimations[i][0], times)
                self.all_estimations[i][1] = np.add(self.all_estimations[i][1], estimations)



    def visualize_and_save(self):
        times, caps = mm.MMReader.get_lists_from_dict(self.capacity_dict, 1000)
        plt.fill_between(times, caps, 0, facecolor='pink', color='pink', alpha=0.3, label='capacity')

        for i in range(2):
            times = self.all_estimations[i][0]
            estimations = self.all_estimations[i][1]
            times = [x / 2 for x in times]
            estimations = [x / 2 for x in estimations]
            plt.plot(times, estimations, label=self.variants[i])

        
        plt.xlabel("time(s)")
        plt.ylabel("throughput(Mbits/s)")
        plt.legend(loc='upper right')

        save_loc = 'vis/saved_images/bw_est_' + self.mm_trace + '_' + self.mm_transport + '_' + self.mm_cc + '.png'
        print('Saving to ' + save_loc)
        plt.savefig(save_loc)

        plt.show()