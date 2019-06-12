from pytdlib.api import functions, types
from ...ext import BaseTelegram


class SetOption(BaseTelegram):

    def set_option(self, name: str, value):
        if value is None:
            value = types.OptionValueEmpty()
        elif isinstance(value, str):
            value = types.OptionValueString(value)
        elif isinstance(value, bool):
            value = types.OptionValueBoolean(value)
        elif isinstance(value, int):
            value = types.OptionValueInteger(value)

        return self.send(
            functions.SetOption(
                name=name,
                value=value
            )
        )
