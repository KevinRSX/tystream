import json
import os
import sys

import ui
import dump_to_config
from front_exceptions import *

supported_trace = ['trace1', 'trace2', 'trace3']
supported_transport = ['tcp', 'quic']
supported_cc = ['cubic', 'bbr']
supported_abr = ['mpc', 'robust_mpc', 'pensieve']

welcome_message = "Welcome to tystream!"
config_incomplete_message = 'Your configuration is incomplete, check config/config.json.\n\
Either edit the config/config.json and run this program again or config all of them manually here.'
cmd_error_message = 'Read ./README.md for use cases of this CLI'

tyui = ui.TystreamUI()

print(welcome_message)
if not tyui.config_complete():
    print(config_incomplete_message)
else:
    print('Configuration: ' + str(tyui.config))

while True:
    try:
        command = input('tystream> ')
        try:
            parse_retval = tyui.parse_command(command)
            if parse_retval[0] == -2: # empty
                continue
            if parse_retval[0] == -1: # exit
                sys.exit(0)
            if parse_retval[0] == 0:
                if (parse_retval[1] == 'trace' and (parse_retval[2] not in supported_trace)) \
                or (parse_retval[1] == 'transport' and (parse_retval[2] not in supported_transport)) \
                or (parse_retval[1] == 'cc' and (parse_retval[2] not in supported_cc)) \
                or (parse_retval[1] == 'abr' and (parse_retval[2] not in supported_abr)):
                    raise ConfigNotSupportedError()
                tyui.set_config(parse_retval[1], parse_retval[2])
        except ArgNotCorrectError as e:
            print(str(e))
            print(cmd_error_message)
        except CommandNotFoundError as e:
            print(str(e))
            print(cmd_error_message)
        except ConfigNotSupportedError:
            print("Config Not Supported. See main.py for supported set of configurations")
    except KeyboardInterrupt:
        sys.exit("Keyboard Interrupt, exiting...")