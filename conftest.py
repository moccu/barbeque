import shutil
import tempfile

import django
import pytest


@pytest.yield_fixture()
def media(request, settings):
    tmpdir = tempfile.mkdtemp()
    settings.MEDIA_ROOT = tmpdir
    yield
    shutil.rmtree(tmpdir)


@pytest.yield_fixture()
def activate_cms(settings):
    settings.ROOT_URLCONF = 'barbeque.tests.cms_urls'
    settings.MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
    )

    if django.VERSION[:2] != (1, 6):
        settings.MIDDLEWARE_CLASSES += (
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        )

    settings.CMS_TEMPLATES = (('empty_template.html', 'empty'),)
    settings.CMS_TOOLBARS = [
        'cms.cms_toolbar.PlaceholderToolbar',
        'cms.cms_toolbar.BasicToolbar',
        'cms.cms_toolbar.PageToolbar',
        'barbeque.cms.toolbar.ForceModalDialogToolbar',
    ]

    yield
