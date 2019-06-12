import logging

from pytdlib.api import functions
from ...ext import BaseTelegram

log = logging.getLogger(__name__)


class DisableProxy(BaseTelegram):

    def disable_proxy(self):
        log.info('Disable Proxy')
        return self.send(
            functions.DisableProxy()
        )
