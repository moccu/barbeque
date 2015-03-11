import os


DEBUG = TEMPLATE_DEBUG = True

SECRET_KEY = 'testing'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'menus',
    'mptt',
    'cms',

    'barbeque',
    'barbeque.tests.resources.mockapp',
)

MIGRATION_MODULES = {
    'cms': 'cms.migrations_django',
    'menus': 'menus.migrations_django',
    'filer': 'filer.migrations_django',
}

ROOT_URLCONF = 'django.contrib.auth.urls'

SITE_ID = 1
LANGUAGES = (('en-us', 'en-us'),)

MIDDLEWARE_CLASSES = []

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'resources', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'barbeque.context_processors.settings',
)
