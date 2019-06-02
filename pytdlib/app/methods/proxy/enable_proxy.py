from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class EnableProxy(BaseTelegram):

    def enable_proxy(self, proxy_id: int=None):
        if proxy_id is None:
            if self._proxy is not None and self._proxy.id is not None:
                proxy_id = self._proxy.id
            else:
                return False
        self.send(functions.EnableProxy(proxy_id))
        return True
