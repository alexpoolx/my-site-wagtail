from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pqov6@@2a=4b@)40gnrzi3ot^u!mi70aiy04*v-4u!7$q0yqd7'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


INTERNAL_IPS = ("127.0.0.1","172.17.0.1")

try:
    from .local import *
except ImportError:
    pass
