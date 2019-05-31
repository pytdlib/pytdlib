class ProxyType:

    def __init__(self, hostname: str, port: int, enabled: bool=False, last_used_date: int=None):
        self.hostname = hostname
        self.port = port
        self.enabled = enabled
        self.last_used_date = last_used_date