from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class PingProxy(BaseTelegram):

    def ping_proxy(self, proxy_id: int):
        return self.send(
            functions.PingProxy(
                proxy_id=proxy_id
            )
        )
