from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class DisableProxy(BaseTelegram):

    def disable_proxy(self):
        return self.send(
            functions.DisableProxy()
        )
