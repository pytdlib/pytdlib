from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class SendCodeRequest(BaseTelegram):

    def send_code_request(self, phone_number: str, flash_call: bool = False):
        return self.send(
            functions.SetAuthenticationPhoneNumber(phone_number, flash_call, False)
        )
