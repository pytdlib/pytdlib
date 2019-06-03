from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class Close(BaseTelegram):

    def close(self):
        self._is_ready = False
        return self.send(functions.Close())
