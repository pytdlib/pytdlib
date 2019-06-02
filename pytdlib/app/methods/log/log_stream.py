from pytdlib.app.utils import BaseTelegram
from pytdlib.app.types import LogStream as Log
from pytdlib.api import functions


class LogStream(BaseTelegram):

    @property
    def log_stream(self) -> 'Log.Default or Log.File or Log.Empty':
        res = self.execute(functions.GetLogStream())
        return Log.parser(res)

    @log_stream.setter
    def log_stream(self, value: 'Log.Default or Log.File or Log.Empty'):

        if isinstance(value, type):
            value = value()

        if not value:
            value = Log.Empty()

        self.execute(functions.SetLogStream(value))
