class CommandNotFoundError(Exception):
    def __init__(self, cmd, message='Command Not Found: '):
        self.cmd = cmd
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message + self.cmd

class ArgNotCorrectError(Exception):
    def __init__(self, arg_for_cmd, message='Argument Not Correct: '):
        self.arg_for_cmd = arg_for_cmd
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message + self.arg_for_cmd

class ConfigNotSupportedError(Exception):
    pass