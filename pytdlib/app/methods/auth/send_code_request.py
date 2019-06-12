from pytdlib.api import functions
from ...ext import BaseTelegram


class SendCodeRequest(BaseTelegram):

    def send_code_request(self, phone_number: str, flash_call: bool = False):
        return self.send(
            functions.SetAuthenticationPhoneNumber(phone_number, flash_call, False)
        )
