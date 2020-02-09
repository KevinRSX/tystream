import sys

class MMReader:
    def __init__(self, file_path, ms_per_bin, expected_duration):
        self.all_capacity = {}
        self.all_departure = {}
        self.MS_PER_BIN = ms_per_bin
        self.duration = None
        self.initial_time = None # system time
        self.base_timestamp = None # first timestamp in log

        with open(file_path, 'r') as f:
            for line in f:
                row = str.split(line)
                # ignore heading lines except for initial timestamp
                if row[0] == '#':
                    if row[1] == "init":
                        self.initial_time = float(row[-1]) / 1000
                    continue
                
                timestamp = float(row[0])
                event_type = row[1]
                num_bytes = int(row[2])
                if len(row) > 3:
                    delay = row[3]
                
                num_bits = num_bytes * 8
                bin = self.ms_to_bin(timestamp)
                if self.base_timestamp == None:
                    self.base_timestamp = timestamp
                
                # three cases: capacity, arrival, departure, while
                # only capacity and departure are dealt with here
                # a chance to send
                if event_type == '#':
                    if bin in self.all_capacity:
                        self.all_capacity[bin] += num_bits
                    else:
                        self.all_capacity[bin] = num_bits
                # arrival, ignored
                elif event_type == '+':
                    continue
                # departure
                elif event_type == '-':
                    if bin in self.all_departure:
                        self.all_departure[bin] += num_bits
                    else:
                        self.all_departure[bin] = num_bits

                if timestamp >= expected_duration:
                    self.duration = (timestamp - self.base_timestamp) / 1000
                    break     
        
        # if actual duration is shorter than expected duration, use the expected one
        # normally won't happen because mahimahi lasts longer than rl_server
        if self.duration == None:
            self.duration = expected_duration / 1000
        
    
    def get_time_list(self, opt):
        # get time list in all_capacity
        if opt == 'cap':
            time_list = list(self.all_capacity.keys())
            time_list = sorted(self.bin_to_seconds(x) for x in time_list)
            return time_list
        else: # all_departure
            time_list = list(self.all_departure.keys())
            time_list = sorted(self.bin_to_seconds(x) for x in time_list)
            return time_list
    
    def get_capacity_list(self):
        t = self.get_time_list("cap")
        cap_list = []
        for key in t:
            cap_list.append(self.all_capacity[key])
        return [x / 1000000 for x in cap_list] # Mbits
    
    def get_departure_list(self):
        t = self.get_time_list("dep")
        dep_list = []
        for key in t:
            dep_list.append(self.all_departure[key])
        return [x / 1000000 for x in dep_list] # Mbits

    @staticmethod
    def get_lists_from_dict(bw_dict, MS_PER_BIN):
        time_list = list(bw_dict.keys())
        time_list = sorted(x * MS_PER_BIN / 1000 for x in time_list)
        bw_list = []
        for key in time_list:
            bw_list.append(bw_dict[key])
        return time_list, [x / 1000000 for x in bw_list]
    
    def ms_to_bin(self, ms):
        return int(ms / self.MS_PER_BIN)
    
    def bin_to_seconds(self, bin):
        return bin * self.MS_PER_BIN / 1000


# test driver
if __name__ == "__main__":
    usage = "python3 mahimahi.py path/to/mm_log MS_PER_BIN expected_time(ms)"
    if len(sys.argv) < 4:
        sys.exit("Usage: " + usage)
    log_path = sys.argv[1]
    MS_PER_BIN = int(sys.argv[2])
    expected_time = int(sys.argv[3])
    r = MMReader(log_path, MS_PER_BIN, expected_time)
    print(r.all_departure)
    print(r.all_capacity)
    print(r.duration)
    print(r.initial_time)