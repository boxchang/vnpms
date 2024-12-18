# VNPMS/settings/test.py

from .base import *

SECRET_KEY = '-e9tzio&ivf94+ek0$_9l8op)gxc4r+t9pen@dov0j7c4zks%r'

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
        'NAME': 'EFGP_Test',
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
        'NAME': 'DC_Dev',
        'USER': 'noah_dev',
        'PASSWORD': 'noah_dev',
        'HOST': '10.96.101.10',
        'PORT': '1433',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}