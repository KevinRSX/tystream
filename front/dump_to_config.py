# initialization
import json

def dump(config_dict=None):
    if config_dict == None:
        config_dict = {
            'trace': 'LTE',
            'transport': 'tcp',
            'cc': 'cubic',
            'abr': 'mpc',
        }
    
    with open('../config/config.json', 'w') as f:
        json.dump(config_dict, f)

if __name__ == '__main__':
    dump()