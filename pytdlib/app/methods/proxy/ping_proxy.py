from pytdlib.api import functions
from ...ext import BaseTelegram


class PingProxy(BaseTelegram):

    def ping_proxy(self, proxy_id: int):
        return self.send(
            functions.PingProxy(
                proxy_id=proxy_id
            )
        )
