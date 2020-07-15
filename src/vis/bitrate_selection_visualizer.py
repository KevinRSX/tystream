from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

from vis.generic_visualizer import GenericVisualizer
import vis.log_reader.rl_server as rl
import exp.abr_name_converter as name_converter

class BitrateSelectionVisualizer(GenericVisualizer):
    def __init__(self, config):
        GenericVisualizer.__init__(self, config)
        self.form_paths()
        self.process_data()
    
    def form_paths(self):
        self.rl_path = []
        self.rl_trace = self.internal_config['trace']
        self.rl_transport = self.internal_config['transport']
        self.rl_cc = self.internal_config['cc']
        self.rl_abr = self.internal_config['abr']

        for i in range(len(self.variants)):
            if self.V == 'abr':
                full_path = self.directories[i] + "log_" + name_converter.to_html(self.rl_abr[i]).split('_')[-1] + '_' + self.rl_transport + '_' + self.rl_cc + '_' + self.rl_trace + '1'
                self.save_loc = 'vis/saved_images/bitrates_' + self.rl_trace + '_' + self.rl_transport + '_' + self.rl_cc + '.png'
            elif self.V == 'cc':
                full_path = self.directories[i] + "log_" + name_converter.to_html(self.rl_abr).split('_')[-1] + '_' + self.rl_transport + '_' + self.rl_cc[i] + '_' + self.rl_trace + '1'
                self.save_loc = 'vis/saved_images/bitrates_' + self.rl_trace + '_' + self.rl_transport + '_' + self.rl_abr + '.png'
            elif self.V == 'transport':
                full_path = self.directories[i] + "log_" + name_converter.to_html(self.rl_abr).split('_')[-1] + '_' + self.rl_transport[i] + '_' + self.rl_cc + '_' + self.rl_trace + '1'
                self.save_loc = 'vis/saved_images/bitrates_' + self.rl_trace + '_' + self.rl_cc + '_' + self.rl_abr + '.png'
            elif self.V == 'trace':
                full_path = self.directories[i] + "log_" + name_converter.to_html(self.rl_abr).split('_')[-1] + '_' + self.rl_transport + '_' + self.rl_cc + '_' + self.rl_trace[i] + '1'
                self.save_loc = 'vis/saved_images/bitrates_' + self.rl_transport + '_' + self.rl_cc + '_' + self.rl_abr + '.png'
            self.rl_path.append(full_path)
    
    def process_data(self):
        self.all_bitrates = []
        for f in self.rl_path:
            reader = rl.RLReader(f)
            self.all_bitrates.append(reader.bitrates)
        


    def visualize_and_save(self):
        for i in range(2):
            plt.plot(self.all_bitrates[i], label=self.variants[i])
        
        plt.xlabel("chunk #")
        plt.ylabel("bitrate (kbps)")
        plt.legend(loc='upper right')

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
