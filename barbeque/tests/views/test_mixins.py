import mock
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
from django.views.generic import View, RedirectView

from barbeque.views.mixins import LoginRequiredMixin, CachePageMixin


class ProtectedView(LoginRequiredMixin, RedirectView):
    permanent = False
    url = '/success/'

protected_view = ProtectedView.as_view()


@pytest.mark.django_db
class TestLoginRequiredMixin:
    def test_not_logged_in(self, rf, settings):
        settings.LOGIN_URL = '/login/'

        request = rf.get('/protected/')
        request.user = AnonymousUser()

        # Simulate MessagesMiddleware and make the user have a session.
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = protected_view(request)
        assert response.status_code == 302
        assert response['Location'] == '/login/?next=/protected/'

    @mock.patch('django.contrib.messages.info')
    def test_not_logged_in_sets_info_message(self, info_func, rf, settings):
        settings.LOGIN_URL = '/login/'

        request = rf.get('/protected/')
        request.user = AnonymousUser()

        # Simulate MessagesMiddleware and make the user have a session.
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = protected_view(request)
        assert response.status_code == 302
        assert response['Location'] == '/login/?next=/protected/'

        assert info_func.call_count == 1

    def test_logged_in(self, rf, settings):
        settings.LOGIN_URL = '/login/'

        request = rf.get('/protected/')
        request.user = get_user_model()(username='testuser')

        response = protected_view(request)
        assert response.status_code == 302
        assert response['Location'] == '/success/'


class CachedView(CachePageMixin, View):
    cache_timeout = 10

    def get(self, *args, **kwargs):
        return HttpResponse()


class TestCachePageMixin:
    def setup(self):
        self.view = CachedView()

    @mock.patch('barbeque.views.mixins._generate_cache_key')
    def test_get_page_cache_key(self, generate_mock, rf):
        request = rf.get('/')
        self.view.get_page_cache_key(request)

        generate_mock.call_args[0] == (
            request, 'GET', [], settings.CACHE_MIDDLEWARE_KEY_PREFIX)

    @mock.patch('barbeque.views.mixins.get_cache')
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

    @mock.patch('barbeque.views.mixins.get_cache')
    def test_get_never_cache(self, cache_mock, rf):
        cache_mock.return_value.get.return_value = None
        self.view.cache_ensure_never_cache = True
        response = self.view.dispatch(rf.get('/'))
        assert 'max-age=0' in response['cache-control']

    @mock.patch('barbeque.views.mixins.get_cache')
    def test_dispatch_no_timeout(self, cache_mock, rf):
        cache_mock.return_value.get.return_value = None
        self.view.cache_timeout = None

        self.view.dispatch(rf.get('/'))
        assert cache_mock.return_value.set.called is False

    @mock.patch('barbeque.views.mixins.get_cache')
    def test_dispatch_set_cache_httpresponse(self, cache_mock, rf):
        cache_mock.return_value.get.return_value = None
        self.view.get = mock.MagicMock(return_value=HttpResponse())

        self.view.dispatch(rf.get('/'))
        assert cache_mock.return_value.set.called is True

    @mock.patch('barbeque.views.mixins.get_cache')
    def test_dispatch_set_cache_templateresponse(self, cache_mock, rf):
        cache_mock.return_value.get.return_value = None
        self.view.get = mock.MagicMock(
            return_value=SimpleTemplateResponse('empty_template.html'))

        self.view.dispatch(rf.get('/')).render()
        assert cache_mock.return_value.set.called is True
