from pytdlib.app.utils import BaseTelegram
from pytdlib.app.types.proxy import ProxyType, Socks5Proxy, HttpProxy, MTprotoProxy
from pytdlib.api import functions
from pytdlib.api import types


class AddProxy(BaseTelegram):

    def add_proxy(self, proxy: ProxyType):
        proxies = {
            Socks5Proxy: lambda p: types.ProxyTypeSocks5(p.username, p.password),
            HttpProxy: lambda p: types.ProxyTypeHttp(p.username, p.password, p.http_only),
            MTprotoProxy: lambda p: types.ProxyTypeMtproto(p.secret)
        }
        return self.send(
            functions.AddProxy(
                server=proxy.hostname,
                port=proxy.port,
                enable=proxy.enabled,
                type=proxies[type(proxy)](proxy)
            )
        )
