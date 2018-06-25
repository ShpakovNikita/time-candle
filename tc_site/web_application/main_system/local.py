# Delete this file on heroku

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'mydb',
                'USER': 'shaft',
                'HOST': '/var/run/postgresql',
                'PASSWORD': '',
                'PORT': '5432'}
}

DEBUG = True

DATABASE_CONFIG = {
            'NAME': 'mydb',
            'USER': 'shaft',
            'HOST': '/var/run/postgresql',
            'PASSWORD': '',
            'PORT': '5432'
}
