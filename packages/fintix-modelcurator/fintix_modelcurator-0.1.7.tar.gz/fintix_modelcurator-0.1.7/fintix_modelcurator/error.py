from fintix_modelcurator.exit_code import *


class FintixError:
    def __init__(self, exception=None, message=None, exit_code=UNKNOWN, should_exit=False):
        self.exception = exception
        self.message = message
        self.exit_code = exit_code
        self.should_exit = should_exit

    def getException(self):
        return self.exception

    def getMessage(self):
        return self.message

    def getExitCode(self):
        return self.exit_code

    def shouldExit(self):
        return self.should_exit