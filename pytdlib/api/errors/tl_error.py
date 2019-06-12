class TLError(Exception):
    """This is the base exception class for all TDLib API related errors.

    Parameters:
        message (``str``)
            message TLError message; subject to future changes
        code (``int``)
            code TLError code; subject to future changes
            If the error code is 406, the error message must not be processed in any way and must not be displayed to the user
    """

    CODE = None
    MESSAGE = None

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.CODE = code
        self.MESSAGE = message
