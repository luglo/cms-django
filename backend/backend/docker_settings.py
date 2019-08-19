# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'integreat',
        'USER': 'integreat',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}
