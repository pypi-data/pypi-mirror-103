# ttldict2
Another dictionary with expiring keys.

## Details
There are quire a few expiring/ttl dictionary libraries available. This one might be a better choice for you if:  
  - Only need support for Python 3.7+ or PyPy3
  - Use it in a single/asyncio thread
  - Work correctly regardless of system-clock adjustments

The implementation is a wrapper around the builtin dict. As a design choice the methods that are not wrapped with
TTL logic are accessible and can be used with caution.

# Install & usage
A source distribution is available on PyPI:

```console
$ python -m pip install ttldict2
```

```pycon
>>> import time
>>> import ttldict2
>>> d = ttldict2.TTLDict(ttl_seconds=1.0)
>>> d["a"] = 5
>>> d.get("a")
5
>>> time.sleep(1.1)
>>> d.get("a")
None
```
