from pytdlib.api import functions, types
from pytdlib.api.errors import TLError
from ...ext import BaseTelegram


class GetOption(BaseTelegram):

    def get_option(self, name: str):
        try:
            return self.options_dict[name]
        except KeyError:
            try:
                option_value = self.send(
                    functions.GetOption(name)
                )
                if isinstance(option_value, types.OptionValueEmpty):
                    value = False
                else:
                    value = option_value.value
                self.options_dict[name] = value
                return value
            except TLError:
                return None
