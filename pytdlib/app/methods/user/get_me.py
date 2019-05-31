from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class GetMe(BaseTelegram):

    def get_me(self):
        return self.send(
            functions.GetMe()
        )
