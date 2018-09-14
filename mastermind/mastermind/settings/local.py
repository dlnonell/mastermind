from .base import *

DEBUG = True

SECRET_KEY = '$o+xx)(xeaz-f@74!4_ko0%v(#h0alntw#=(pj+1t3yc7oa^o^'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}