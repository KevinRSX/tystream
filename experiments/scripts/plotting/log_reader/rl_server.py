import sys

class RLReader:
    def __init__(self, rl_log_path):
        self.num_chunks = 0
        self.timestamps = []
        self.estimations = []
        self.all_qoe = []

        with open(rl_log_path, 'r') as f:
            first_line = f.readline() # comment this if you need to read the first line
            for line in f:
                self.num_chunks += 1
                row = str.split(line)
                if len(row) <= 0:
                    continue # skip blank lines
                self.timestamps.append(float(row[0]))
                self.estimations.append(float(row[-2]) / 1000)
                self.all_qoe.append(float(row[-1]))
        
        self.mean_qoe = sum(self.all_qoe) / self.num_chunks

    
    # calculate relative timestamps by subtracting mahimahi init_timestamp
    def relative_timestamps(self, init_timestamp):
        return [x - init_timestamp for x in self.timestamps]
    

# test driver
if __name__ == "__main__":
    usage = "python3 mahimahi.py path/to/rlserver_log init_timestamp"
    if len(sys.argv) < 3:
        sys.exit("Usage: " + usage)
    log_path = sys.argv[1]
    init_timestamp = float(sys.argv[2])
    r = RLReader(log_path)
    print(r.num_chunks)
    print(r.timestamps)
    print(r.estimations)
    print(r.all_qoe)
    print(r.mean_qoe)
    print(r.relative_timestamps(init_timestamp))