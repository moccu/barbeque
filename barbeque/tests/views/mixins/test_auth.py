import mock
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.views.generic import RedirectView

from barbeque.views.mixins.auth import LoginRequiredMixin


class ProtectedView(LoginRequiredMixin, RedirectView):
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

        assert info_func.assert_called_once()

    def test_logged_in(self, rf, settings):
        settings.LOGIN_URL = '/login/'

        request = rf.get('/protected/')
        request.user = get_user_model()(username='testuser')

        response = protected_view(request)
        assert response.status_code == 301
        assert response['Location'] == '/success/'
