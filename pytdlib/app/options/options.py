class Options:
    """Contains Options for TDLib,
    TDLib has many options that affect the behavior of the library.
    Each option has a name and a value. Value may be ``str``, ``int``, ``bool``.

    Attributes:
        animation_search_bot_username (``str``)
            Username of a bot which can be used in inline mode for animations search
        authorization_date (``int``)
            Point in time (Unix timestamp) when authorization was received
        basic_group_size_max (``int``)
            Maximum number of members in a basic group
        call_connect_timeout_ms (``int``)
            Maximum time to wait for call connection creation to be passed to libtgvoip
        call_packet_timeout_ms (``int``)
            Maximum time to wait for call packet delivery to be passed to libtgvoip
        enabled_proxy_id (``int``):
            Identifier of the enabled proxy
        expect_blocking (``bool`)
            If True, access to Telegram is likely blocked for the user
        favorite_stickers_limit (``int``)
            Maximum number of favorite stickers
        forwarded_message_count_max (``int``)
            Maximum number of forwarded messages per one request
        message_caption_length_max (``int``)
            Maximum length of a message caption
        message_text_length_max (``int``)
            Maximum length of a message text
        my_id (``int``)
            Identifier of the current user
        pinned_chat_count_max (``int``)
            Maximum number of pinned cloud chats. The same amount of secret chats can be pinned locally
        photo_search_bot_username (``str``)
            Username of a bot which can be used in inline mode for photos search
        suggested_language_pack_id (``int``)
            Identifier of the language pack, suggested for the user by the server
        supergroup_size_max (``int``)
            Maximum number of members in a supergroup
        t_me_url (``str``)
            Current value of t.me URL, i.e. https://t.me/
        test_mode (``bool``)
            If True, the test environment is being used instead of the production environment
        venue_search_bot_username (``str``)
            Username of a bot which can be used in inline mode for venues search
        version (``iny``)
            TDLib version. This options is guaranteed to come before all other updates since TDLib 1.4.0

    Parameters:
        disable_contact_registered_notifications (``bool``)
            If True, notifications about the user's contacts who have joined Telegram will be disabled.
            User will still receive the corresponding message in the private chat. getOption needs to be called explicitly
            to fetch latest value of the option, changed from another device.
        disable_top_chats (``bool``)
            If True, support for top chats and statistics collection is disabled.
        ignore_background_updates (``bool``)
            If True, allows to skip all updates received while the TDLib instance was not running.
            The option does nothing if the database or secret chats are used
        language_pack_database_path (``str``)
            Path to a database for storing language pack strings, so that this database can be shared between different accounts.
            By default, language pack strings are stored only in memory.
        language_pack_id (``str``)
            Identifier of the currently used language pack from the current localization target
        localization_target (``str``)
            Name for the current localization target (currently supported: “android”, “android_x”, “ios”, “macos” and “tdesktop”)
        notification_group_count_max (``int``)
            Maximum number of notification groups to be shown simultaneously, 0-25
        notification_group_size_max (``int``)
            Maximum number of simultaneously shown notifications in a group, 1-25. Defaults to 10
        online (``bool``)
            Online status of the current user
        prefer_ipv6 (``bool``)
            If True, IPv6 addresses will be preferred over IPv4 addresses
        use_pfs (``bool``)
            If True, Perfect Forward Secrecy will be enabled for interaction with the Telegram servers for cloud chats
        use_quick_ack (``bool``)
            If True, quick acknowledgement will be enabled for outgoing messages
        use_storage_optimizer (``bool``)
            If True, the background storage optimizer will be enabled

    Notes:
        Attributes aren't Writable,
        Additionally any option beginning with ‘x’ or ‘X’ is writeable and can be safely used by the application to
        persistently store some small amount of data.
    """
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

    def __init__(self,
                 disable_contact_registered_notifications : bool=None,
                 disable_top_chats: bool=None,
                 ignore_background_updates: bool=None,
                 ignore_inline_thumbnails: bool=None,
                 language_pack_database_path: str=None,
                 language_pack_id: str=None,
                 localization_target: str=None,
                 notification_group_count_max: int=None,
                 notification_group_size_max: int=None,
                 online: bool=None,
                 prefer_ipv6: bool=None,
                 use_pfs: bool=None,
                 use_quick_ack: bool=None,
                 use_storage_optimizer: bool=None):
        self.disable_contact_registered_notifications = disable_contact_registered_notifications
        self.disable_top_chats = disable_top_chats
        self.ignore_background_updates = ignore_background_updates
        self.ignore_inline_thumbnails = ignore_inline_thumbnails
        self.language_pack_database_path = language_pack_database_path
        self.language_pack_id = language_pack_id
        self.localization_target = localization_target
        self.notification_group_count_max = notification_group_count_max
        self.notification_group_size_max = notification_group_size_max
        self.online = online
        self.prefer_ipv6 = prefer_ipv6
        self.use_pfs = use_pfs
        self.use_quick_ack = use_quick_ack
        self.use_storage_optimizer = use_storage_optimizer
