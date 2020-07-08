class Emulator:
    def __init__(self, trace, log):
        self.trace = trace
        self.log = log
    
    def trace_location(self):
        return './cooked_traces/' + self.trace
    
    def log_location(self, id):
        return './results/' + self.log + str(id)
    
    def generate_emulation_cmd(self, id):
        trace_loc = self.trace_location()
        log_loc = self.log_location(id)
        cmd_mm = "mm-delay 40 mm-link --uplink-log=./results/uplink --downlink-log=" \
        + log_loc + " ./cooked_traces/12mbps " + trace_loc + ".down"
        return cmd_mm