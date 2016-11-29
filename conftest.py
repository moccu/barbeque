import shutil
import tempfile

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
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
    )

    settings.CMS_TEMPLATES = (('empty_template.html', 'empty'),)
    settings.CMS_TOOLBARS = [
        'cms.cms_toolbars.PlaceholderToolbar',
        'cms.cms_toolbars.BasicToolbar',
        'cms.cms_toolbars.PageToolbar',
        'barbeque.cms.toolbar.ForceModalDialogToolbar',
        'barbeque.tests.resources.cmsapp.cms_toolbars.ExtensionToolbar',
    ]

    yield
