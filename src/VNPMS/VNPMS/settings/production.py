# VNPMS/settings/production.py

from .base import *

PROD = True

SECRET_KEY = '8i7h&)&2z!$!e710^%m)i4f(7_lpn)8ofu8&)djhix$q^66k0s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'BPM': {
        'ENGINE': 'mssql',
        'NAME': 'NaNa',
        'USER': 'sa',
        'PASSWORD': '134',
        'HOST': '10.96.101.4',
        'PORT': '1433',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
    'DC': {
        'ENGINE': 'mssql',
        'NAME': 'DC',
        'USER': 'noah',
        'PASSWORD': 'noah',
        'HOST': '10.96.101.10',
        'PORT': '1433',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}