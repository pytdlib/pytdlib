from pytdlib.api import functions, types
from ...ext import BaseTelegram, proxy_parser
from ...types import ProxyType, Socks5Proxy, HttpProxy, MTprotoProxy


class AddProxy(BaseTelegram):

    def add_proxy(self, proxy: ProxyType):
        proxies = {
            Socks5Proxy: lambda p: types.ProxyTypeSocks5(p.username, p.password),
            HttpProxy: lambda p: types.ProxyTypeHttp(p.username, p.password, p.http_only),
            MTprotoProxy: lambda p: types.ProxyTypeMtproto(p.secret)
        }
        res = self.send(
            functions.AddProxy(
                server=proxy.hostname,
                port=proxy.port,
                enable=proxy.enabled,
                type=proxies[type(proxy)](proxy)
            )
        )
        return proxy_parser(res)
