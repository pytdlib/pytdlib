from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class LogVerbosity(BaseTelegram):

    @property
    def log_verbosity(self) -> int:
        res = self.execute(functions.GetLogVerbosityLevel())
        return res.verbosity_level

    @log_verbosity.setter
    def log_verbosity(self, value: int):
        self.execute(functions.SetLogVerbosityLevel(value))
