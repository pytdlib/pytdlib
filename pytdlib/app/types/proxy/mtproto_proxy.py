from .proxy import ProxyType


class MTprotoProxy(ProxyType):

    def __init__(self,
                 hostname: str,
                 port: int,
                 secret: str,
                 enabled: bool = True,
                 **kwargs):
        super(MTprotoProxy, self).__init__(hostname, port, enabled, **kwargs)
        self.secret = secret
