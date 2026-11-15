# Memory-Serve

[![CI](https://github.com/kapildhinwa2010-dev/Memory-Serve/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/Memory-Serve/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kapildhinwa2010-dev/Memory-Serve/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/Memory-Serve/actions/workflows/codeql.yml)

Serve memory lookups through an LRU cache with eviction and hit/miss statistics.

## What it does

CacheService is an in-process LRU cache: at most capacity entries, least
recently used eviction, recency refreshed on hits. serve() wraps a
lookup with a request id and latency, and stats track hits, misses and
evictions.

    from memory_serve import CacheService

    cache = CacheService(capacity=128)
    cache.put("key", value)
    out = cache.serve("req-1", "key")
    print(out["hit"], out["value"], out["latency_ms"])

## API

- CacheService(capacity) - put / get / serve / len / stats
- ServeRegistry - the generic base registry (unchanged from DNA-Serve)

## Honest results and limitations

- Purely in-process and single-threaded; not a distributed cache and not
  thread-safe.
- Eviction is strict LRU over insert/access order; no TTL, no size-based
  eviction by object size.
- Values are held by reference: mutating a stored object mutates the
  cache content.

## Status

Part of the kapildhinwa2010-dev toolkit experiments. CI and CodeQL run on
every push to main. License: MIT.
