import ui
import unittest
import os
import dump_to_config

class TestUI(unittest.TestCase):
    def test_config_nofile(self):
        tyui = ui.TystreamUI()
        if os.path.isfile('../config/config.json'):
            os.remove('../config/config.json')
        self.assertEqual(tyui.config_complete(), False)

    def test_config_ok(self):
        tyui = ui.TystreamUI()
        dump_to_config.dump()
        self.assertEqual(tyui.config_complete(), True)

    def test_config_lessfile(self):
        tyui = ui.TystreamUI()
        dump_to_config.dump({
            'transport': 'tcp',
            'cc': 'cubic',
            'abr': 'mpc',
        })
        self.assertEqual(tyui.config_complete(), False)
    
    def test_parse_command(self):
        tyui = ui.TystreamUI()
        self.assertEqual(tyui.parse_command(''), [-2])

if __name__ == '__main__':
    unittest.main()
