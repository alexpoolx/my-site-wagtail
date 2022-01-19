from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pqov6@@2a=4b@)40gnrzi3ot^u!mi70aiy04*v-4u!7$q0yqd7'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['https://my-site-wagtail.herokuapp.com'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
