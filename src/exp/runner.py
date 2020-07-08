from abc import ABC, abstractmethod

class Runner(ABC):
    def __init__(self, config, run_times):
        self.trace = config['trace']
        self.abr = config['abr']
        self.cc = config['cc']
        self.transport = config['transport']
        self.run_times = run_times
    
    @abstractmethod
    def set_commands(self):
        pass

    @abstractmethod
    def run(self):
        pass
