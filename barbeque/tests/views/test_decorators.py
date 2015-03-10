import pytest
from django.http import HttpResponse

from barbeque.views.decorators import ssl_required


class TestSSLRequired:
    @pytest.fixture(autouse=True)
    def setup(self, settings):
        settings.DEBUG = False
        settings.BARBEQUE_SSL_ENABLED = True

        self.view = ssl_required(lambda r: HttpResponse(''))

    def test_insecure_get_request(self, rf):
        request = rf.get('/test/', data={'next': '/target/'})

        response = self.view(request)
        assert response.status_code == 302

        expected_url = 'https://testserver/test/?next=%2Ftarget%2F'
        assert response['Location'] == expected_url

    def test_insecure_post_request(self, rf):
        request = rf.post('/test/', data={'next': '/target/'})

        response = self.view(request)
        assert response.status_code == 405

    def test_secure_request(self, rf):
        request = rf.get('/test/')
        request.is_secure = lambda: True

        response = self.view(request)
        assert response.status_code == 200

    def test_insecure_get_request_ssl_disabled(self, settings, rf):
        settings.BARBEQUE_SSL_ENABLED = False

        request = rf.get('/test/', data={'next': '/target/'})

        response = self.view(request)
        assert response.status_code == 200

    def test_insecure_post_request_ssl_disabled(self, settings, rf):
        settings.BARBEQUE_SSL_ENABLED = False

        request = rf.post('/test/', data={'next': '/target/'})

        response = self.view(request)
        assert response.status_code == 200
