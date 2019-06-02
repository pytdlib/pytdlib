from .add_proxy import AddProxy
from .ping_proxy import PingProxy
from .get_proxies import GetProxies
from .remove_proxy import RemoveProxy
from .enable_proxy import EnableProxy
from .disable_proxy import DisableProxy


class Proxy(
    AddProxy,
    PingProxy,
    GetProxies,
    RemoveProxy,
    EnableProxy,
    DisableProxy
):
    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        if not value:
            self.disable_proxy()
        else:
            self._proxy = self.add_proxy(value)

    @proxy.deleter
    def proxy(self):
        self.disable_proxy()
