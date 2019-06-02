from pytdlib import Error
from ..types import Options


class TlOptions(Options):

    animation_search_bot_username = None
    authorization_date = None
    basic_group_size_max = None
    call_connect_timeout_ms = None
    call_packet_timeout_ms = None
    enabled_proxy_id = None
    expect_blocking = None
    favorite_stickers_limit = None
    forwarded_message_count_max = None
    message_caption_length_max = None
    message_text_length_max = None
    my_id = None
    pinned_chat_count_max = None
    photo_search_bot_username = None
    suggested_language_pack_id = None
    supergroup_size_max = None
    t_me_url = None
    test_mode = None
    venue_search_bot_username = None
    version = None
    calls_enabled = None

    NOT_WRITEABLE = {
        'animation_search_bot_username',
        'authorization_date',
        'basic_group_size_max',
        'call_connect_timeout_ms',
        'call_packet_timeout_ms',
        'enabled_proxy_id',
        'expect_blocking',
        'favorite_stickers_limit',
        'forwarded_message_count_max',
        'message_caption_length_max',
        'message_text_length_max',
        'my_id',
        'pinned_chat_count_max',
        'photo_search_bot_username',
        'suggested_language_pack_id',
        'supergroup_size_max',
        't_me_url',
        'test_mode',
        'venue_search_bot_username',
        'version'
    }

    def __init__(self, setattr, getattr):
        Options.__setattr__ = setattr
        Options.__getattribute__ = getattr

    def __setattr__(self, key, value):
        if key in TlOptions.NOT_WRITEABLE:
            raise Error(3, 'Option can\'t be set')
        return Options.__setattr__(key, value)

    def __getattr__(self, item):
        return Options.__getattribute__(item)
