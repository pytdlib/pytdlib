from pytdlib.api import functions
from ...ext import BaseTelegram, proxy_parser


class GetProxies(BaseTelegram):

    def get_proxies(self):
        res = self.send(
            functions.GetProxies(
            )
        )
        return [proxy_parser(proxy) for proxy in res.proxies]
