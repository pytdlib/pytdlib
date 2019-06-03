from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions
from pytdlib.api import types


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
