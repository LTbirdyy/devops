from app.config import settings

if settings.TESTING:
    # Em testes/CI, usamos um Redis falso em memória para não depender
    # de um servidor Redis real rodando.
    import fakeredis

    redis_client = fakeredis.FakeStrictRedis(decode_responses=True)
else:
    import redis

    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_cached_url(short_code: str):
    """Busca a URL original no cache. Retorna None se não estiver cacheada."""
    return redis_client.get(short_code)


def set_cached_url(short_code: str, original_url: str):
    """Guarda a URL original no cache com um TTL configurável."""
    redis_client.setex(short_code, settings.CACHE_TTL_SECONDS, original_url)
