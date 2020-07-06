from abc import ABC, abstractmethod

class Runner(ABC):
    def __init__(self, trace, abr, run_times):
        self.trace = trace
        self.abr = abr
        self.run_times = run_times
    
    @abstractmethod
    def set_all_commands():
        pass

    @abstractmethod
    def run():
        pass
