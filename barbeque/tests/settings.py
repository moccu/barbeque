import os

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'barbeque',

    'barbeque.tests.resources.mockapp',
)

ROOT_URLCONF = 'django.contrib.auth.urls'

MIDDLEWARE_CLASSES = []

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'resources', 'templates'),
)
