import time
import pytest

from ttldict2 import TTLDict

T = 0.1


def test_ttldict():
    def values(d_):
        return [ttl_value.value for ttl_value in d_.values()]

    with pytest.raises(ValueError):
        TTLDict()
    with pytest.raises(ValueError):
        TTLDict(max_items=0)
    with pytest.raises(ValueError):
        TTLDict(ttl_seconds=0)

    d = TTLDict(max_items=12, ttl_seconds=T * 2.0)

    time.sleep(T * 0.5)
    for i in range(0, 5):
        d[i] = 1 + i
    assert values(d) == [1, 2, 3, 4, 5]

    time.sleep(T * 1)
    for i in range(5, 10):
        d[i] = 1 + i
    assert values(d) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for i in range(0, 10):
        assert d[i] == 1 + i
    assert values(d) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    time.sleep(T * 1)
    assert values(d) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # eat_old has not been called
    assert d.get(-1) is None
    assert d.get(-1, -1) == -1
    assert d.get(-1, d) is d
    assert values(d) == [6, 7, 8, 9, 10]
    for i in range(0, 5):
        with pytest.raises(KeyError):
            _ = d[i]
        assert d.get(i) is None
        assert d.get(i, -1) == -1
        assert d.get(i, d) is d
    assert values(d) == [6, 7, 8, 9, 10]
    for i in range(5, 10):
        assert d[i] == 1 + i
    assert values(d) == [6, 7, 8, 9, 10]

    time.sleep(T * 1.5)
    assert values(d) == [6, 7, 8, 9, 10]
    assert d.get(-1) is None
    assert d.get(-1, -1) == -1
    assert d.get(-1, d) is d
    assert values(d) == []
    for i in range(0, 10):
        with pytest.raises(KeyError):
            _ = d[i]
        assert d.get(i) is None
        assert d.get(i, -1) == -1
        assert d.get(i, d) is d
    assert values(d) == []

    for i in range(0, 5):
        with pytest.raises(KeyError):
            d.pop(i)
        with pytest.raises(KeyError):
            del d[i]
        assert d.pop(i, None) is None
    assert values(d) == []

    for i in range(0, 5):
        assert values(d) == []
        d[i] = 1 + i
        assert values(d) == [1 + i]
        assert d.pop(i) == 1 + i
        assert values(d) == []
        assert i not in d
        assert values(d) == []

    for i in range(0, 5):
        assert values(d) == []
        d[i] = 1 + i
        assert values(d) == [1 + i]
        del d[i]
        assert values(d) == []
        assert i not in d
        assert values(d) == []

    # touch
    for i in range(0, 5):
        d[i] = 1 + i
    assert values(d) == [1, 2, 3, 4, 5]
    time.sleep(T * 1)
    for i in range(0, 5):
        d.get(i, touch=bool(i % 2))
    assert d.get(10, touch=True) is None
    assert values(d) == [1, 3, 5, 2, 4]
    time.sleep(T * 1.5)
    assert values(d) == [1, 3, 5, 2, 4]
    assert d.get(-1) is None
    assert values(d) == [2, 4]
    time.sleep(T * 2.5)
    assert values(d) == [2, 4]
    assert d.get(-1) is None
    assert values(d) == []

    # test ttl drop after update
    d[5] = 7
    time.sleep(T * 1.5)
    d[5] = 8
    time.sleep(T)
    d.drop_old_items()
    time.sleep(T * 2)
    assert d.get(5) is None
    assert values(d) == []

    for i in range(0, 15):
        d[i] = 1 + i
    assert values(d) == [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    d[7] = 8
    assert values(d) == [4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 8]
