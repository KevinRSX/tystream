from abc import ABC, abstractmethod

class GenericVisualizer(ABC):
    def __init__(self, config):
        for key, value in config.items():
            if isinstance(value, list) and key != 'dir':
                self.variants = value
            if key == 'dir':
                self.directories = value
    
    @abstractmethod
    def form_paths(self):
        # form file paths from variants and directories
        pass

    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    def visualize_and_save(self):
        pass