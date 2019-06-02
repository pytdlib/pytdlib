from .socks5_ptoxy import Socks5Proxy


class HttpProxy(Socks5Proxy):

    def __init__(self,
                 hostname: str,
                 port: int,
                 enabled: bool=True,
                 username: str=None,
                 password: str=None,
                 http_only: bool=False,
                 **kwargs):
        super(HttpProxy, self).__init__(hostname, port, enabled, username, password, **kwargs)
        self.http_only = http_only
