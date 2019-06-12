from pytdlib.api import functions
from ...ext import BaseTelegram


class GetMe(BaseTelegram):

    def get_me(self):
        return self.send(
            functions.GetMe()
        )
