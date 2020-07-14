from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

from vis.generic_visualizer import GenericVisualizer
import vis.log_reader.rl_server as rl
import exp.abr_name_converter as name_converter

class QoeVisualizer(GenericVisualizer):
    def __init__(self, config):
        GenericVisualizer.__init__(self, config)
        self.form_paths()
        self.process_data()
    
    def form_paths(self):
        self.rl_path = []
        self.rl_trace = 'ATT-LTE-driving'
        self.rl_transport = 'quic'
        self.rl_cc = 'cubic'
        for i in range(len(self.variants)):
            full_path = self.directories[i] + "log_" + name_converter.to_html(self.variants[i]).split('_')[-1] + '_' + self.rl_transport + '_' + self.rl_cc + '_' + self.rl_trace + '1'
            self.rl_path.append(full_path)
    
    def process_data(self):
        self.all_qoe = []
        for f in self.rl_path:
            reader = rl.RLReader(f)
            self.all_qoe.append(reader.all_qoe)
        


    def visualize_and_save(self):
        for i in range(2):
            plt.plot(self.all_qoe[i], label=self.variants[i])
        
        plt.xlabel("chunk #")
        plt.ylabel("QoE")
        plt.legend(loc='upper right')


        save_loc = 'vis/saved_images/qoe_' + self.rl_trace + '_' + self.rl_transport + '_' + self.rl_cc + '.png'
        print('Saving to ' + save_loc)
        plt.savefig(save_loc)

        plt.show()
