import logging
from .authorization_stats import AuthorizationStats

log = logging.getLogger(__name__)

try:
    import ujson as json
    log.info("Using ujson")
except ImportError:
    import json


def object_to_bytes(query: bytes or dict or str) -> bytes:
    """convert object to bytes

    Parameters:
        query (``bytes`` | ``dict`` | ``str``)

    Returns:
        ``bytes`` : converted query to bytes
    """
    if isinstance(query, bytes):
        return query
    elif isinstance(query, dict):
        return json.dumps(query).encode('utf-8')
    elif isinstance(query, str):
        return query.encode('utf-8')
    else:
        return bytes(query)
