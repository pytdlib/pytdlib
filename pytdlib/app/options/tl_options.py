from pytdlib import TLError
from .options import Options


class TLOptions(Options):

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
        if key in TLOptions.NOT_WRITEABLE:
            raise TLError(3, 'Option can\'t be set')
        return super().__setattr__(key, value)

    def __getattr__(self, item):
        return super().__getattribute__(item)

    def __setitem__(self, key, value):
        return self.__setattr__(key, value)

    def __getitem__(self, item):
        return self.__getattr__(item)
