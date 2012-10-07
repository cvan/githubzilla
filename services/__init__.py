import sys
sys.path.append('..')

try:
    import settings_local as settings
except ImportError:
    import settings

from redis import Redis


redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASS
)
