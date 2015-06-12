from __future__ import absolute_import

from anylink.extensions import BaseLink
from cms.models.fields import PageField
from cms.utils import get_cms_setting
from django.core.cache import cache
from django.db import models
from django.utils.six.moves.urllib import parse as urlparse
from django.utils.translation import get_language, ugettext_lazy as _


class CmsPageLink(BaseLink):
    name = 'page'
    verbose_name = _('CMS Page')
    provided_fields = ('page', 'anchor')

    def configure_model(self, model):
        model.add_to_class(
            self.get_name(), PageField(blank=True, null=True))
        model.add_to_class(
            'anchor', models.CharField(max_length=256, null=True, blank=True))

    def get_absolute_url(self, link):
        cache_key = '{0}anylink-page-url:{1}:{2}'.format(
            get_cms_setting('CACHE_PREFIX'), str(link.page_id), get_language())

        url = cache.get(cache_key)
        if url is None:
            url = link.page.get_absolute_url()
            cache.set(cache_key, url, get_cms_setting('CACHE_DURATIONS')['content'])

        if link.anchor:
            parsed = urlparse.urlparse(url)
            parsed = parsed._replace(fragment=link.anchor)
            url = parsed.geturl()

        return url
