from pytdlib.api import Object
from functools import total_ordering


@total_ordering
class AuthorizationStats:
        STATS = [
            'authorizationStateWaitTdlibParameters',
            'authorizationStateWaitEncryptionKey',
            'authorizationStateWaitPhoneNumber',
            'authorizationStateWaitCode',
            'authorizationStateWaitPassword',
            'authorizationStateReady',
            'authorizationStateClosing',
            'authorizationStateClosed',
            'authorizationStateLoggingOut',
        ]

        def __init__(self, step: int or str):
            if isinstance(step, int):
                self.step = step - 1 if step > 0 else range(len(AuthorizationStats.STATS))[step]
            else:
                self.step = AuthorizationStats.STATS.index(step)

        def __eq__(self, other):
            step = self.get_step(other)
            return step == self.step

        def __lt__(self, other):
            step = self.get_step(other)
            return self.step < step

        @staticmethod
        def get_step(d):
            if isinstance(d, int):
                return d
            elif isinstance(d, str):
                return AuthorizationStats.STATS.index(d)
            elif isinstance(d, Object):
                return AuthorizationStats.STATS.index(d.ID)
            else:
                return
