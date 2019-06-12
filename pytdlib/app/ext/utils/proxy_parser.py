from pytdlib.api import types
from ...types import Socks5Proxy, HttpProxy, MTprotoProxy


def proxy_parser(proxy):
    kwargs = dict(
        id=proxy.id,
        hostname=proxy.server,
        port=proxy.port,
        last_used_date=proxy.last_used_date,
        enabled=proxy.is_enabled
    )
    proxies = {
        types.ProxyTypeSocks5: lambda p: (Socks5Proxy, dict(username=p.username, password=p.password)),
        types.ProxyTypeHttp: lambda p: (HttpProxy, dict(username=p.username, password=p.password, http_only=p.http_only)),
        types.ProxyTypeMtproto: lambda p: (MTprotoProxy, dict(secret=p.secret))
    }
    p_type, ex_kwargs = proxies[type(proxy.type)](proxy.type)
    return p_type(**{**kwargs, **ex_kwargs})
