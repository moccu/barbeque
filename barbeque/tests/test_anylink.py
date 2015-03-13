from __future__ import absolute_import

import mock
import pytest
from anylink.models import AnyLink
from cms.api import create_page
from django.core.cache import cache

from barbeque.anylink import CmsPageLink


@pytest.mark.django_db
@pytest.mark.usefixtures('activate_cms')
class TestCmsPageLink:
    def setup(self):
        cache.clear()
        root = create_page('Root Page', 'INHERIT', 'en-us')
        self.page = create_page('Sub page', 'INHERIT', 'en-us', parent=root)

    def test_get_absolute_url(self):
        link = AnyLink(link_type='page', page=self.page)

        url = CmsPageLink().get_absolute_url(link)

        assert url == '/sub-page/'

    def test_get_absolute_url_cache_hit(self):
        link = AnyLink(link_type='page', page=self.page)

        url = CmsPageLink().get_absolute_url(link)
        assert url == '/sub-page/'

        with mock.patch('cms.models.Page.get_absolute_url') as url_mock:
            url_mock.return_value = '/not-cached/'

            url = CmsPageLink().get_absolute_url(link)
            assert url_mock.called is False
            assert url == '/sub-page/'

    def test_get_absolute_url_with_anchor(self):
        link = AnyLink(link_type='page', page=self.page, anchor='section')

        url = CmsPageLink().get_absolute_url(link)

        assert url == '/sub-page/#section'
