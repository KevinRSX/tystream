from abc import ABC, abstractmethod

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
        self.internal_config['trace'] = exp_config['trace']
        self.internal_config['transport'] = exp_config['transport']
        self.internal_config['cc'] = exp_config['cc']
        self.internal_config['abr'] = exp_config['abr']
        self.internal_config[self.V] = self.variants
        print(bcolors.UNDERLINE + 'Fixed network parameters are set to the experiment config of last run' + bcolors.ENDC)
        print(bcolors.OKGREEN + str(self.internal_config) + bcolors.ENDC)
