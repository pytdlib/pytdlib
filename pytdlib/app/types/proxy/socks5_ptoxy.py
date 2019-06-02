from .proxy import ProxyType


class Socks5Proxy(ProxyType):

    def __init__(self,
                 hostname: str,
                 port: int,
                 enabled: bool = True,
                 username: str=None,
                 password: str=None,
                 **kwargs):
        super(Socks5Proxy, self).__init__(hostname, port, enabled, **kwargs)
        self.username = username
        self.password = password
