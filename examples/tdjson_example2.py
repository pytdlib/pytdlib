#
# rewrited tdjson_example.py (https://github.com/tdlib/td/blob/master/example/python/tdjson_example.py)
# from td project (https://github.com/tdlib/td) in pytdlib!
#

from pytdlib.td import TD
from pytdlib.api import Object, functions
from ctypes.util import find_library
from ctypes import CDLL
import sys

# load shared library
tdjson_path = find_library("tdjson") or "tdjson.dll"
if tdjson_path is None:
    print('can\'t find tdjson library')
    quit()
td_json = CDLL(tdjson_path)

# load json app
app_json = TD(td_json)


# initialize log with desired parameters
def on_fatal_error_callback(error_message):
    print('TDLib fatal error: ', error_message)


app_json.log.set_verbosity_level(0)
app_json.log.set_fatal_error_callback(on_fatal_error_callback)

# create client
app_json.client.create()


# testing TDLib execute method
print(app_json.client.execute(functions.GetTextEntities('@telegram /test_command https://telegram.org telegram.me', extra= ['5', 7.0])))
# testing TDLib send method
app_json.client.send(functions.GetAuthorizationState(extra=1.01234))

# main events cycle
while True:
    event = app_json.client.receive(timeout=1.0)
    if event:
        # get extra value from event
        extra = event.get("@extra", None)

        event = Object.read(event)
        # if client is closed, we need to destroy it and create new client
        if event.ID == 'updateAuthorizationState' and event.authorization_state.ID == 'authorizationStateClosed':
            break

        print(event)
        # handle an incoming update or an answer to a previously sent request
        sys.stdout.flush()

# destroy client when it is closed and isn't needed anymore
app_json.close()
