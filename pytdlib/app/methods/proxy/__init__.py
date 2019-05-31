from .add_proxy import AddProxy
from .ping_proxy import PingProxy
from .get_proxies import GetProxies
from .remove_proxy import RemoveProxy


class Proxy(
    AddProxy,
    PingProxy,
    GetProxies,
    RemoveProxy
):
    pass
