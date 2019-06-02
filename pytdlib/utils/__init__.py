import logging
from .authorization_stats import authorization_stats

log = logging.getLogger(__name__)

try:
    import ujson as json
    log.info("Using ujson")
except ImportError:
    import json


def object_to_bytes(query):
    if isinstance(query, bytes):
        return query
    elif isinstance(query, dict):
        return json.dumps(query).encode('utf-8')
    elif isinstance(query, str):
        return query.encode('utf-8')
    else:
        return bytes(query)
