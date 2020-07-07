import json
import os
import sys

from front.front_exceptions import *

class TystreamUI:
    def __init__(self):
        self.config = {}

    def config_complete(self):
        config_path = '../config/config.json'
        if not os.path.isfile(config_path):
            return False
        with open(config_path, 'r') as f:
            config = json.load(f)
        if ('trace' not in config) or ('transport' not in config) or ('cc' not in config) or ('abr' not in config):
            return False
        else:
            self.config = config
            return True

    def parse_command(self, command):
        '''
        Returns:
        [-2]: empty
        -1: exit
        [0, config_key, config_value]: configuration
        [1, running times, saving_loc]: run experiment
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
                return [0, cmd_list[1], cmd_list[2]]
            else:
                raise ArgNotCorrectError(cmd_list[0])    
        elif cmd_list[0] == 'exp':
            if len(cmd_list) != 3:
                raise ArgNotCorrectError(cmd_list[0])
            try:
                run_time = int(cmd_list[1])
            except ValueError:
                raise ArgNotCorrectError(cmd_list[0])
            return [1, run_time, cmd_list[2]]
        elif cmd_list[0] == 'plot':
            if len(cmd_list) != 2:
                raise ArgNotCorrectError(cmd_list[0])
            return [2, cmd_list[1]]
        else:
            raise CommandNotFoundError(cmd_list[0])
    
    def set_config(self, key, value):
        self.config[key] = value
        print(key + " is set to " + value)
        print('Configuration: ' + str(self.config))

