import os
import mock

import pytest
from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.conf.urls import url

from barbeque.static import ServeStaticFileMiddleware


def foo_view(request):
    return redirect('bar', permanent=True)


def bar_view(request):
    return HttpResponse('Hllo FooBar!')


urlpatterns = [
    url(r'^bar$', bar_view, name='bar'),
    url(r'^foo$', foo_view, name='foo'),

]


class TestServeStaticFileMiddleware:

    @pytest.fixture(autouse=True)
    def setup(self, settings):
        settings.ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
        settings.STATIC_ROOT = os.path.join(settings.ROOT_DIR, 'tests', 'resources', 'static')

    @pytest.fixture
    def patch_settings(self, settings):
        """
        Patch settings for tests fith django client
        """
        settings.STATICFILES_FINDERS = (
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            'compressor.finders.CompressorFinder',
        )
        settings.MIDDLEWARE_CLASSES = [
            'barbeque.static.ServeStaticFileMiddleware',
        ]
        settings.INSTALLED_APPS = settings.INSTALLED_APPS + ('django.contrib.staticfiles',)
        settings.ROOT_URLCONF = 'barbeque.tests.test_static'

    def test_file_exists(self, rf):
        request = rf.get('/static/test.jpg')
        middleware = ServeStaticFileMiddleware()
        response = middleware.process_response(request, HttpResponseNotFound(''))
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/jpeg'
        assert len(response.items()) == 3
        assert response.has_header('Content-Length')
        assert response.has_header('Last-Modified')

    def test_file_missing(self, rf):
        request = rf.get('/static/doesnotexist.jpg')
        middleware = ServeStaticFileMiddleware()
        response = middleware.process_response(request, HttpResponseNotFound(''))
        assert response.status_code == 404

    def test_unknown_prefix(self, rf):
        request = rf.get('/foo/test.jpg')
        middleware = ServeStaticFileMiddleware()
        response = middleware.process_response(request, HttpResponseNotFound(''))
        assert response.status_code == 404

    def test_redirect_for_static(self, rf):
        request = rf.get('/static/test.jpg')
        middleware = ServeStaticFileMiddleware()
        response = middleware.process_response(
            request, HttpResponsePermanentRedirect('/static/test.jpg/'))
        assert response.status_code == 200

    def test_redirect_other(self, rf):
        request = rf.get('/foo')
        middleware = ServeStaticFileMiddleware()
        redirect = HttpResponsePermanentRedirect('/foo/')
        response = middleware.process_response(request, redirect)
        assert response == redirect

    @mock.patch('barbeque.static.ServeStaticFileMiddleware.process_response')
    def test_new_style_middleware(self, process_response_mock, rf):
        request = rf.get('/static/test.jpg')
        get_response_mock = mock.Mock()
        get_response_mock.return_value = HttpResponseNotFound()
        middleware = ServeStaticFileMiddleware(get_response=get_response_mock)
        middleware(request)
        get_response_mock.assert_called_with(request)
        process_response_mock.assert_called_with(
            request, get_response_mock.return_value)

    def test_with_client_hit(self, client, patch_settings):
        response = client.get('/static/test.jpg')
        assert response.status_code == 200

    def test_with_client_redirect(self, client, patch_settings):
        response = client.get('/foo')
        assert response.status_code == 301
        assert response['Location'].endswith('/bar')

    def test_with_client_query_params(self, client, patch_settings):
        response = client.get('/static/test.jpg?v=1')
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/jpeg'
