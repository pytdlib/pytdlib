from pytdlib.app.utils import BaseTelegram
from pytdlib.app.utils.proxy_parser import proxy_parser
from pytdlib.api import functions


class GetProxies(BaseTelegram):

    def get_proxies(self):
        res = self.send(
            functions.GetProxies(
            )
        )
        return [proxy_parser(proxy) for proxy in res.proxies]
