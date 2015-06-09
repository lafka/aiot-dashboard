from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'aiot_data',
        'USER': 'dag',
        'PASSWORD': 'digi123',
        'HOST': 'dag.monsternett.no',
    }
}
