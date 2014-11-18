import mock
from django.conf import settings
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
from django.views.generic import View

from barbeque.views.mixins.cache import CachePageMixin


class TestView(CachePageMixin, View):
    cache_timeout = 10

    def get(self, *args, **kwargs):
        return HttpResponse()


class TestCachePageMixin:
    def setup(self):
        self.view = TestView()

    @mock.patch('barbeque.views.mixins.cache._generate_cache_key')
    def test_get_page_cache_key(self, generate_mock, rf):
        request = rf.get('/')
        self.view.get_page_cache_key(request)

        generate_mock.assert_called_with(
            request, 'GET', [], settings.CACHE_MIDDLEWARE_KEY_PREFIX)

    @mock.patch('barbeque.views.mixins.cache.get_cache')
    def test_get(self, cache_mock, rf):
        cache_mock.return_value.get.return_value = None
        self.view.get = mock.MagicMock(return_value=HttpResponse())

        response = self.view.dispatch(rf.get('/'))
        assert response['cache-control'] == 'max-age=10'
        assert self.view.get.call_count == 1

        # Cache hit
        cache_mock.return_value.get.return_value = response
        self.view.dispatch(rf.get('/'))
        assert self.view.get.call_count == 1

    @mock.patch('barbeque.views.mixins.cache.get_cache')
    def test_get_never_cache(self, cache_mock, rf):
        cache_mock.return_value.get.return_value = None
        self.view.cache_ensure_never_cache = True
        response = self.view.dispatch(rf.get('/'))
        assert response['cache-control'] == 'max-age=0'

    @mock.patch('barbeque.views.mixins.cache.get_cache')
    def test_dispatch_no_timeout(self, cache_mock, rf):
        cache_mock.return_value.get.return_value = None
        self.view.cache_timeout = None

        self.view.dispatch(rf.get('/'))
        assert cache_mock.return_value.set.called is False

    @mock.patch('barbeque.views.mixins.cache.get_cache')
    def test_dispatch_set_cache_httpresponse(self, cache_mock, rf):
        cache_mock.return_value.get.return_value = None
        self.view.get = mock.MagicMock(return_value=HttpResponse())

        self.view.dispatch(rf.get('/'))
        assert cache_mock.return_value.set.called is True

    @mock.patch('barbeque.views.mixins.cache.get_cache')
    def test_dispatch_set_cache_templateresponse(self, cache_mock, rf):
        cache_mock.return_value.get.return_value = None
        self.view.get = mock.MagicMock(
            return_value=SimpleTemplateResponse('empty_template.html'))

        self.view.dispatch(rf.get('/')).render()
        assert cache_mock.return_value.set.called is True
