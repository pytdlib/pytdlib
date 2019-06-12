from pytdlib.api import functions
from ...ext import BaseTelegram


class SignUp(BaseTelegram):

    def sign_up(self, code: str, first_name: str, last_name: str = ""):
        return self.send(functions.CheckAuthenticationCode(code, first_name, last_name))

