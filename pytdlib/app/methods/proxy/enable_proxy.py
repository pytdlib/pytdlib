import logging

from pytdlib.api import functions
from ...ext import BaseTelegram

log = logging.getLogger(__name__)


class EnableProxy(BaseTelegram):

    def enable_proxy(self, proxy_id: int=None):
        if proxy_id is None:
            if self._proxy is not None and self._proxy.id is not None:
                proxy_id = self._proxy.id
            else:
                return False
        log.info('Enable Proxy')
        self.send(functions.EnableProxy(proxy_id))
        return True
