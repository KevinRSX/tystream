from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

from vis.generic_visualizer import GenericVisualizer
import vis.log_reader.mahimahi as mm

class LinkUtilVisualizer(GenericVisualizer):
    def __init__(self, config):
        GenericVisualizer.__init__(self, config)
        self.form_paths()
        self.process_data()
    
    def form_paths(self):
        # self.mm_path = []
        # self.mm_trace = 'Verizon-LTE-short'
        # self.mm_transport = 'quic'
        # self.mm_cc = 'cubic'
        # for i in range(len(self.variants)):
        #     full_path = self.directories[i] + self.mm_trace + '_' + self.mm_transport + '_' + self.mm_cc + '_' + self.variants[i]
        #     self.mm_path.append(full_path)
        self.mm_path = []
        self.mm_trace = self.internal_config['trace']
        self.mm_transport = self.internal_config['transport']
        self.mm_cc = self.internal_config['cc']
        self.mm_abr = self.internal_config['abr']
        for i in range(len(self.variants)):
            if self.V == 'abr':
                full_path = self.directories[i] + self.mm_trace + '_' + self.mm_transport + '_' + self.mm_cc + '_' + self.mm_abr[i]
                self.save_loc = 'vis/saved_images/link_util_' + self.mm_trace + '_' + self.mm_transport + '_' + self.mm_cc + '.png'
            elif self.V == 'transport':
                full_path = self.directories[i] + self.mm_trace + '_' + self.mm_transport[i] + '_' + self.mm_cc + '_' + self.mm_abr
                self.save_loc = 'vis/saved_images/link_util_' + self.mm_trace + '_' + self.mm_cc + '_' + self.mm_abr + '.png'
            elif self.V == 'trace':
                full_path = self.directories[i] + self.mm_trace[i] + '_' + self.mm_transport + '_' + self.mm_cc + '_' + self.mm_abr
                self.save_loc = 'vis/saved_images/link_util_' + self.mm_transport + '_' + self.mm_cc + '_' + self.mm_abr + '.png'
            elif self.V == 'cc':
                full_path = self.directories[i] + self.mm_trace + '_' + self.mm_transport + '_' + self.mm_cc[i] + '_' + self.mm_abr
                self.save_loc = 'vis/saved_images/link_util_' + self.mm_trace + '_' + self.mm_transport + '_' + self.mm_abr + '.png'
            self.mm_path.append(full_path)

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
        


    def visualize_and_save(self):
        times, caps = mm.MMReader.get_lists_from_dict(self.capacity_dict, 1000)
        plt.fill_between(times, caps, 0, facecolor='pink', color='pink', alpha=0.3, label='capacity')

        for i in range(2):
            times, dept = mm.MMReader.get_lists_from_dict(self.bw_dict[i], 1000)
            dept = [x / 2 for x in dept]
            print("Utilization of capacity of " + self.variants[i] + " = " + '{:.3f}'.format(np.sum(dept) / np.sum(caps)))
            plt.plot(times, dept, label=self.variants[i])
        
        plt.xlabel("time(s)")
        plt.ylabel("throughput(Mbits/s)")
        plt.legend(loc='upper right')

        # save_loc = 'vis/saved_images/link_util_' + self.mm_trace + '_' + self.mm_transport + '_' + self.mm_cc + '.png'
        print('Saving to ' + self.save_loc)
        plt.savefig(self.save_loc)

        plt.show()

        

if __name__ == '__main__':
    luv = LinkUtilVisualizer(
        {
            "trace": "fixed",
            "transport": "fixed",
            "cc": "fixed",
            "abr": ["mpc", "robustmpc"],
            "dir": ["exp/result/", "exp/result/"]
        }
    )
    luv.form_paths()
