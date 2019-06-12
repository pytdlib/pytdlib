from pytdlib.api import functions
from ...ext import BaseTelegram


class RemoveProxy(BaseTelegram):

    def remove_proxy(self, proxy_id: int):
        return self.send(
            functions.RemoveProxy(
                proxy_id=proxy_id
            )
        )
