import json
import os
import sys

from front.front_exceptions import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class TystreamUI:
    def __init__(self):
        self.exp_config = {}
        self.plot_config = {}
        
        with open('../config/supported.json', 'r') as f:
            self.supported = json.load(f)
        # self.supported_trace = supported['supported_trace']
        # self.supported_transport = supported['supported_transport']
        # self.supported_cc = supported['supported_cc']
        # self.supported_abr = supported['supported_abr']

    def get_config_from_file(self, file_path):
        if not os.path.isfile(file_path):
            return None
        with open(file_path, 'r') as f:
            config = json.load(f)
        return config

    def exp_config_complete(self, config):
        if config == None:
            return False
        if ('trace' not in config) or ('transport' not in config) or ('cc' not in config) or ('abr' not in config):
            return False
        else:
            self.exp_config = config
            return True
    
    def exp_config_supported(self, key, value):
        # tells if an exp configuration key-value pair is supported
        # returns boolean
        return (value in self.supported[key])
    
    def plot_config_complete(self, config):
        # does not check support
        if config == None:
            return False
        num_fixed = 0
        len_variable = 0
        num_dir = 0
        if ('trace' not in config) or ('transport' not in config) or ('cc' not in config) or ('abr' not in config) or ('dir' not in config):
            return False
        
        for key, value in config.items():
            if value == 'fixed':
                num_fixed += 1
            elif key == 'dir':
                num_dir = len(config[key])
            else:
                len_variable = len(config[key])
        if (num_fixed != 3) or (len_variable != num_dir):
            return False
        else:
            self.plot_config = config
            return True

    def plot_config_supported(self, config):
        for key, value in config.items():
            if value != 'fixed' and key != 'dir':
                for concrete_parameter in value:
                    if concrete_parameter not in self.supported[key]:
                        return False
        return True

        
        
    def parse_command(self, command):
        '''
        Returns:
        [-2]: empty
        -1: exit
        [0, config_key, config_value]: configuration
        [1, run_time]: run experiment
        [2, plot_args]: plots
        Raise exceptions: command problems
        '''
        cmd_list = command.split(' ')
        if cmd_list[0] == '':
            return [-2]
        if cmd_list[0] == 'quit' or cmd_list[0] == 'exit':
            return [-1]
        elif cmd_list[0] == 'config':
            if len(cmd_list) != 3:
                raise ArgNotCorrectError(cmd_list[0])
            if (cmd_list[1] == 'trace') or (cmd_list[1] == 'transport') or (cmd_list[1] == 'cc') or (cmd_list[1] == 'abr'):
                if not self.exp_config_supported(cmd_list[1], cmd_list[2]):
                    raise ConfigNotSupportedError()
                return [0, cmd_list[1], cmd_list[2]]
            else:
                raise ArgNotCorrectError(cmd_list[0])    
        elif cmd_list[0] == 'exp':
            if len(cmd_list) != 2:
                raise ArgNotCorrectError(cmd_list[0])
            try:
                run_time = int(cmd_list[1])
            except ValueError:
                raise ArgNotCorrectError(cmd_list[0])
            return [1, run_time]
        elif cmd_list[0] == 'plot':
            supported_vis = ['link_utilization', 'bitrate_selection', 'bandwidth_estimation', 'qoe']
            # plot, or
            # plot link_utilization, or
            # plot var abr 2 mpc pensieve, or
            # plot dir 2 dir1 dir2
            if len(cmd_list) == 1:
                return [2] # plot link util by default
            elif len(cmd_list) == 2 and (cmd_list[1] in supported_vis):
                return [2, cmd_list[1]]
            elif cmd_list[1] != 'var' and cmd_list[1] != 'dir':
                raise ArgNotCorrectError(cmd_list[0])
            elif cmd_list[1] == 'var':
                if (cmd_list[2] == 'trace') or (cmd_list[2] == 'transport') or (cmd_list[2] == 'cc') or (cmd_list[2] == 'abr'):
                    try:
                        var_parameter = cmd_list[2]
                        len_variable = int(cmd_list[3])
                    except ValueError:
                        raise ArgNotCorrectError(cmd_list[0])
                    if len(cmd_list) != 4 + len_variable:
                        raise ArgNotCorrectError(cmd_list[0])
                    # Parameters other than var are set to fixed.
                    # Must be supported, but could be incomplete
                    # because users may want to change number of variables & directories
                    temp_plot_config = self.plot_config
                    for key, value in temp_plot_config.items():
                        if key != var_parameter and key != 'dir':
                            temp_plot_config[key] = 'fixed'
                        elif key == var_parameter:
                            temp_plot_config[key] = cmd_list[-len_variable:]
                    print(temp_plot_config)
                    if self.plot_config_supported(temp_plot_config):
                        self.set_plot_config(temp_plot_config)
                        return [2, 'CONFIG']
                    else:
                        raise ConfigNotSupportedError()
                else:
                    raise ArgNotCorrectError(cmd_list[0])
            elif cmd_list[1] == 'dir':
                try:
                    len_dir = int(cmd_list[2])
                except ValueError:
                    raise ArgNotCorrectError(cmd_list[0])
                if len(cmd_list) != 3 + len_dir:
                    raise ArgNotCorrectError(cmd_list[0])
                temp_plot_config = self.plot_config
                temp_plot_config['dir'] = cmd_list[-len_dir:]
                self.set_plot_config(temp_plot_config)
                return [2, 'CONFIG']

        else:
            raise CommandNotFoundError(cmd_list[0])
    
    def set_exp_config(self, key, value):
        self.exp_config[key] = value
        print(key + " is set to " + value)
        print('Experiment configuration: ' + str(self.exp_config))
    
    def set_plot_config(self, config):
        self.plot_config = config
        print('Visualization configuration set to: ' + str(self.plot_config))
        if not self.plot_config_complete(self.plot_config):
            # did not use warnings.warn because it prints only once
            print(bcolors.WARNING + "Warning: Note that the visualization configuration is not complete. " + \
                "You won't be able to process and visualize the evaluation results until you align variable with directory correctly" + bcolors.ENDC)