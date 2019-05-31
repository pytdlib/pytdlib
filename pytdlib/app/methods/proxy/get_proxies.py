from pytdlib.app.utils import BaseTelegram
from pytdlib.app.types.proxy import ProxyType, Socks5Proxy, HttpProxy, MTprotoProxy
from pytdlib.api import functions
from pytdlib.api import types


class GetProxies(BaseTelegram):

    def get_proxies(self):
        return self.send(
            functions.GetProxies(
            )
        )
