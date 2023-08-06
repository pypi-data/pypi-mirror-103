"""
:copyright: 2021 Nándor Mátravölgyi
:license: Apache2, see LICENSE for more details.
"""
import time
from typing import Optional


class _TTLDictEntry(object):
    """
    Minimal memory footprint item for storing the expiration time.
    """

    __slots__ = ("value", "expires")

    def __init__(self, value, expires):
        self.value = value
        self.expires = expires


class TTLDict(dict):
    """
    Simple dictionary with expiring items of the same life-length. Old items are removed implicitly when
    accessing the dictionary through the supported API.
    This implementation builds on the fact that the builtin dict preserves insertion order. (python 3.7+)

    Only the most relevant subset of the dictionary API is wrapped with the TTL logic. Iterator methods can't
    be wrapped easily for example, because the TTL logic needs to mutate the dict during the iteration. They
    are left usable as-is.

    Not thread-safe!
    """

    __slots__ = ("ttl_seconds", "max_items")

    def __init__(self, ttl_seconds: float, max_items: Optional[int] = None):
        if not isinstance(ttl_seconds, float) or ttl_seconds <= 0.0:
            raise ValueError("The value %s is invalid as ttl_seconds for TTLDict" % (ttl_seconds,))
        if max_items is not None and (not isinstance(max_items, int) or max_items < 1):
            raise ValueError("The value %s is invalid as max_items for TTLDict" % (max_items,))
        dict.__init__(self)
        self.ttl_seconds = ttl_seconds
        self.max_items = max_items

    def drop_old_items(self):
        ttl_now = time.perf_counter()
        item_view = self.items()
        while item_view:
            key, ttl_value = item_view.__iter__().__next__()
            if ttl_value.expires >= ttl_now:
                break
            dict.__delitem__(self, key)

    def __setitem__(self, key, value):
        ttl_value = dict.pop(self, key, None)
        if ttl_value is None:
            ttl_value = _TTLDictEntry(value, time.perf_counter() + self.ttl_seconds)
            if self.max_items is not None:
                cull = len(self) - self.max_items
                if cull >= 0:
                    key_iter = iter(self)
                    for old_key in [next(key_iter) for _ in range(1 + cull)]:
                        dict.__delitem__(self, old_key)
        else:
            ttl_value.value = value
            ttl_value.expires = time.perf_counter() + self.ttl_seconds
        dict.__setitem__(self, key, ttl_value)

    def __getitem__(self, key):
        self.drop_old_items()
        return dict.__getitem__(self, key).value

    def pop(self, key, *default):
        self.drop_old_items()
        try:
            return dict.pop(self, key).value
        except KeyError:
            if default:
                return default[0]
            raise

    def get(self, key, default=None, touch=False):
        self.drop_old_items()
        if touch:
            ttl_value = dict.pop(self, key, None)
            if ttl_value is None:
                return default
            ttl_value.expires = time.perf_counter() + self.ttl_seconds
            dict.__setitem__(self, key, ttl_value)
            return ttl_value.value
        try:
            return dict.__getitem__(self, key).value
        except KeyError:
            return default
