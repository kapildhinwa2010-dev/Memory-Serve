"""Tests for Memory-Serve CacheService: LRU cache with stats."""

import pytest

from memory_serve import CacheService, ServeRegistry


def test_put_get_hit_and_miss():
    cache = CacheService(capacity=4)
    cache.put("a", 1)
    hit, value = cache.get("a")
    assert hit and value == 1
    hit2, value2 = cache.get("missing")
    assert not hit2 and value2 is None
    assert cache.stats["hits"] == 1 and cache.stats["misses"] == 1


def test_lru_eviction_order():
    cache = CacheService(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)
    assert not cache.get("b")[0]
    assert cache.get("a")[0] and cache.get("c")[0]
    assert cache.stats["evictions"] == 1


def test_put_same_key_updates_without_eviction():
    cache = CacheService(capacity=2)
    cache.put("a", 1)
    cache.put("a", 2)
    assert len(cache) == 1
    assert cache.get("a") == (True, 2)
    assert cache.stats["evictions"] == 0


def test_serve_wraps_get_with_latency():
    cache = CacheService()
    cache.put("k", [1, 2])
    out = cache.serve("r1", "k")
    assert out["hit"] is True and out["value"] == [1, 2]
    assert out["latency_ms"] >= 0.0


def test_validation():
    with pytest.raises(ValueError):
        CacheService(capacity=0)
    cache = CacheService()
    with pytest.raises(ValueError):
        cache.put("", 1)
    with pytest.raises(ValueError):
        cache.serve("", "k")


def test_base_registry_still_works():
    assert ServeRegistry().summary()["models"] == 0
