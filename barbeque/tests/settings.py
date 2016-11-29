import os
import tempfile


DEBUG = True

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
    'compressor',
    'easy_thumbnails',
    'filer',
    'anylink',
    'treebeard',

    'barbeque',
    'barbeque.tests.resources.mockapp',
    'barbeque.tests.resources.cmsapp',
)

ROOT_URLCONF = 'django.contrib.auth.urls'

SITE_ID = 1
LANGUAGES = (('en-us', 'en-us'),)

MEDIA_ROOT = tempfile.mkdtemp()
MEDIA_URL = '/media/'

STATIC_ROOT = tempfile.mkdtemp()
STATIC_URL = '/static/'

MIDDLEWARE_CLASSES = []

ANYLINK_EXTENSIONS = (
    'anylink.extensions.ExternalLink',
    'barbeque.anylink.CmsPageLink',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'resources', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.core.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'barbeque.context_processors.settings',
            ],
        },
    },
]
