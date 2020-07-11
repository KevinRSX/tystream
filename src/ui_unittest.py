import unittest
import os

import front.ui as ui
from front.front_exceptions import *

class TestUI(unittest.TestCase):
    def test_config_nofile(self):
        tyui = ui.TystreamUI()
        if os.path.isfile('../config/config.json'):
            os.remove('../config/config.json')
        self.assertEqual(tyui.get_config_from_file('../config/config.json'), None)

    def test_exp_config_ok(self):
        tyui = ui.TystreamUI()
        exp_config = tyui.get_config_from_file('../config/exp_config.json')
        self.assertEqual(tyui.exp_config_complete(exp_config), True)
    
    def test_plot_config_ok(self):
        tyui = ui.TystreamUI()
        plot_config = tyui.get_config_from_file('../config/plot_config.json')
        self.assertEqual(tyui.plot_config_complete(plot_config), True)
    
    def test_config_with_error(self):
        tyui = ui.TystreamUI()
        error_dict_exp = {
            "trace": "Verizon-LTE-driving",
            "cc": "cubic",
            "abr": "mpc"
        }
        self.assertEqual(tyui.plot_config_complete(error_dict_exp), False)
        error_dict_plot1 = {
            "trace": "fixed",
            "cc": "fixed",
            "abr": ["mpc", "robust_mpc"],
            "dir": ["exp/result", "exp/result"]
        }
        self.assertEqual(tyui.plot_config_complete(error_dict_plot1), False)
        error_dict_plot2 = {
            "trace": "fixed",
            "transport": "fixed",
            "cc": "fixed",
            "abr": ["mpc", "robustmpc", "pensieve"],
            "dir": ["exp/result", "exp/result"]
        }
        self.assertEqual(tyui.plot_config_complete(error_dict_plot2), False)
        error_dict_plot3 = {
            "trace": "fixed",
            "transport": ["tcp", "quic"],
            "cc": "fixed",
            "abr": ["mpc", "robustmpc"],
            "dir": ["exp/result", "exp/result"]
        }
        self.assertEqual(tyui.plot_config_complete(error_dict_plot3), False)
    
    def test_exp_support(self):
        tyui = ui.TystreamUI()
        exp_config = tyui.get_config_from_file('../config/exp_config.json')
        for key, value in exp_config.items():
            self.assertEqual(tyui.exp_config_supported(key, value), True)
        self.assertEqual(tyui.exp_config_supported('trace', 'ATT-LTE-short'), False)
    
    def test_plot_support(self):
        tyui = ui.TystreamUI()
        plot_config = tyui.get_config_from_file('../config/plot_config.json')
        self.assertEqual(tyui.plot_config_supported(plot_config), True)
        error_but_supported_dict_plot = {
            "trace": "fixed",
            "transport": ["tcp", "quic"],
            "cc": "fixed",
            "abr": ["mpc", "robustmpc"],
            "dir": ["exp/result", "exp/result"]
        }
        self.assertEqual(tyui.plot_config_supported(error_but_supported_dict_plot), True)
        correct_but_not_supported_dict_plot = {
            "trace": "fixed",
            "transport": "fixed",
            "cc": "fixed",
            "abr": ["mpc", "robust mpc"],
            "dir": ["exp/result", "exp/result"]
        }
        self.assertEqual(tyui.plot_config_supported(correct_but_not_supported_dict_plot), False)

    def test_parse_command_nullstring(self):
        tyui = ui.TystreamUI()
        self.assertEqual(tyui.parse_command(''), [-2])

    def test_exit(self):
        tyui = ui.TystreamUI()
        self.assertEqual(tyui.parse_command('exit'), [-1])
        self.assertEqual(tyui.parse_command('quit'), [-1])
    
    def test_user_config_errors(self):
        tyui = ui.TystreamUI()
        self.assertRaises(ArgNotCorrectError, tyui.parse_command, 'config hello')
        self.assertRaises(ArgNotCorrectError, tyui.parse_command, 'config net mpc')
        self.assertRaises(ConfigNotSupportedError, tyui.parse_command, 'config transport udp')
        self.assertRaises(ConfigNotSupportedError, tyui.parse_command, 'config transport udp')

        self.assertRaises(ArgNotCorrectError, tyui.parse_command, 'exp 1 run')
        self.assertRaises(ArgNotCorrectError, tyui.parse_command, 'exp trace')

        self.assertRaises(ArgNotCorrectError, tyui.parse_command, 'plot config abr mpc robustmpc')
        self.assertRaises(ArgNotCorrectError, tyui.parse_command, 'plot var abr mpc robustmpc')
        self.assertRaises(ArgNotCorrectError, tyui.parse_command, 'plot dir abr mpc robustmpc')
        self.assertRaises(ArgNotCorrectError, tyui.parse_command, 'plot dir 2 d1 d2 d3')
        self.assertRaises(ArgNotCorrectError, tyui.parse_command, 'plot var abr 2 mpc robustmpc pensieve')

    
    def test_successful_config(self):
        tyui = ui.TystreamUI()
        self.assertEqual(tyui.parse_command('config transport quic'), [0, 'transport', 'quic'])

    def test_successful_exp(self):
        tyui = ui.TystreamUI()
        self.assertEqual(tyui.parse_command('exp 5'), [1, 5])
    
    def test_successful_exp(self):
        tyui = ui.TystreamUI()
        self.assertEqual(tyui.parse_command('plot'), [2])
        self.assertEqual(tyui.parse_command('plot var trace 2 Verizon-LTE-short ATT-LTE-driving'), [2, 'CONFIG'])

    

if __name__ == '__main__':
    unittest.main()
