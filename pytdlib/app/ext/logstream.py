from pytdlib.api import types


class LogStream:
    class Default(types.LogStreamDefault): pass

    class Empty(types.LogStreamEmpty): pass

    class File(types.LogStreamFile):
        def __init__(self, path: str='TDLib.log', max_file_size: int=1000):
            self.path = path
            self.max_file_size = max_file_size

    @classmethod
    def parser(cls, log_stream):
        if isinstance(log_stream, types.LogStreamDefault):
            return cls.Default()
        elif isinstance(log_stream, types.LogStreamEmpty):
            return cls.Empty()
        elif isinstance(log_stream, types.LogStreamFile):
            return cls.File(log_stream.path, log_stream.max_file_size)
