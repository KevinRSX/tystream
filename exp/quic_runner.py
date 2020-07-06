import abc
import os

class QuicRunner(Runner):
    def __init__(self, trace, abr, run_times):
        Runner.__init__(self, trace, abr)

    def set_all_commands():
        # cmd_client: command that fires up chrome
        # cmd_run: command that runs the script
        self.cmd_run = "python run_quic_traces.py Verizon-LTE-driving test 1"
        pass

    def run():
        pass