from pytdlib.api import functions
from ...ext import BaseTelegram


class CheckBotToken(BaseTelegram):

    def check_bot_token(self, token: str):
        return self.send(
            functions.CheckAuthenticationBotToken(token)
        )
