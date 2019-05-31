from .proxy import ProxyType


class MTprotoProxy(ProxyType):

    def __init__(self, hostname: str, port: int, secret: str, enabled: bool = True):
        super(MTprotoProxy, self).__init__(hostname, port, enabled)
        self.secret = secret
