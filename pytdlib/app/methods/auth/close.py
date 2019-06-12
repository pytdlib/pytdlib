from pytdlib.api import functions
from ...ext import BaseTelegram


class Close(BaseTelegram):

    def close(self):
        self._is_ready = False
        return self.send(functions.Close())
