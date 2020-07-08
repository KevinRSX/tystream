import abc
import os

from exp.runner import Runner

class QuicRunner(Runner):
    def __init__(self, config, run_times):
        Runner.__init__(self, config, run_times)
        self.set_commands()

    def set_commands(self):
        self.cmd_run = "python run_quic_traces.py " + str(self.trace) + \
             " " + self.trace + "_quic_" + self.cc + "_" + self.abr + " " + \
             str(self.run_times)
        pass

    def run(self):
        exec_dir = os.getcwd()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(current_dir)
        os.system(self.cmd_run)
        os.chdir(exec_dir)