from .base import *
DEBUG = True

# print sql to the console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        }
    },
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'post',
        'USER':'post',
        'PASSWORD': 'michal1',
    }
}
# DATABASE_URL = 'postgres://username:password@localhost:5432/post'