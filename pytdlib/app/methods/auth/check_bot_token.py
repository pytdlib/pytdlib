from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class CheckBotToken(BaseTelegram):

    def check_bot_token(self, token: str):
        return self.send(
            functions.CheckAuthenticationBotToken(token)
        )
