from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'aiot',
        'USER': 'aiot',
        'PASSWORD': 'aiot',
        'HOST': 'localhost',
    }
}
