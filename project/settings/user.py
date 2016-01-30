from development import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 1,
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'PICKLE_VERSION': -1,
        },
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

