from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class RemoveProxy(BaseTelegram):

    def remove_proxy(self, proxy_id: int):
        return self.send(
            functions.RemoveProxy(
                proxy_id=proxy_id
            )
        )
