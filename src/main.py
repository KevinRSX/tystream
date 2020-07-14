import json
import os
import sys

import front.ui as ui
import front.dump_to_config as dump_to_config
import exp.quic_runner as quic_runner
import exp.tcp_runner as tcp_runner
import vis.link_util_visualizer as link_util_visualizer
import vis.bitrate_selection_visualizer as bitrate_selection_visualizer
import vis.bandwidth_estimation_visualizer as bandwidth_estimation_visualizer
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

welcome_message = "Welcome to tystream!"
exp_config_incomplete_message = 'Your experiment configuration is incomplete or incorrect, check config/.\n\
Either edit config files in config/ and run this program again or config all of them manually here.'
plot_config_incomplete_message = 'Your visualization configuration is incomplete or incorrect, check config/.\n\
Either edit config files in config/ and run this program again or config all of them manually here.'
cmd_error_message = 'Read ./README.md for use cases of this CLI'

tyui = ui.TystreamUI()

print(welcome_message)

# check & load configuration files to tyui.config
exp_config = tyui.get_config_from_file('../config/exp_config.json')
plot_config = tyui.get_config_from_file('../config/plot_config.json')

if not tyui.exp_config_complete(exp_config):
    print(plot_config_incomplete_message)
else:
    print('Experiment configuration: ' + str(tyui.exp_config))

if not tyui.plot_config_complete(plot_config):
    print(plot_config_incomplete_message)
else:
    print('Visualization configuration: ' + str(tyui.plot_config))


while True:
    try:
        command = input('tystream> ')
        try:
            parse_retval = tyui.parse_command(command)
            if parse_retval[0] == -2: # empty
                continue
            if parse_retval[0] == -1: # exit
                sys.exit(0)
            if parse_retval[0] == 0: # config
                tyui.set_exp_config(parse_retval[1], parse_retval[2])
            if parse_retval[0] == 1: # run exp
                if not tyui.exp_config_complete(tyui.exp_config):
                    raise ConfigIncompleteError('exp')
                for key, value in tyui.exp_config.items():
                    if not tyui.exp_config_supported(key, value):
                        raise ConfigNotSupportedError()
                run_time = parse_retval[1]
                if tyui.exp_config['transport'] == 'quic':
                    runner = quic_runner.QuicRunner(tyui.exp_config, parse_retval[1])
                    runner.run()
                elif tyui.exp_config['transport'] == 'tcp':
                    runner = tcp_runner.TCPRunner(tyui.exp_config, parse_retval[1])
                    runner.run()
                
            if parse_retval[0] == 2: # vis
                if len(parse_retval) > 1: # configure plotting parameters
                    continue
                else:
                    print('Start Visualization..\n' + bcolors.OKGREEN + "Visualization arguments: " + str(tyui.plot_config) + bcolors.ENDC)
                    vis = bandwidth_estimation_visualizer.BandwidthEstimationVisualizer(tyui.plot_config)
                    vis.visualize_and_save()

        except ArgNotCorrectError as e:
            print(str(e))
            print(cmd_error_message)
        except CommandNotFoundError as e:
            print(str(e))
            print(cmd_error_message)
        except ConfigNotSupportedError:
            print("Config Not Supported. See config/supported.json for supported set of configurations")
        except ConfigIncompleteError as e:
            print(str(e))
    except KeyboardInterrupt:
        sys.exit("Keyboard Interrupt, exiting...")