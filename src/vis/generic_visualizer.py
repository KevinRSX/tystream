from abc import ABC, abstractmethod

class GenericVisualizer(ABC):
    def __init__(self, config):
        for key, value in config.items():
            if isinstance(value, list) and key != 'dir':
                self.variants = value
                self.V = key
            if key == 'dir':
                self.directories = value
        self.internal_config = {
            'trace': 'ATT-LTE-driving',
            'transport': 'quic',
            'cc': 'cubic',
            'abr': 'mpc'
        }
        self.internal_config[self.V] = self.variants
    
    @abstractmethod
    def form_paths(self):
        # form file paths from variants and directories
        pass

    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    def visualize_and_save(self):
        pass

    def set_internal_config(self, exp_config):
        print("Saving the configuration of last run to internal visualization configuration..")