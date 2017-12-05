import os
import mock
from collections import OrderedDict

import pytest
from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.conf.urls import url
from django.utils.text import force_text

from barbeque.staticfiles.css import transform_css_urls
from barbeque.staticfiles.loader import load_staticfile
from barbeque.staticfiles.middleware import ServeStaticFileMiddleware


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
        # settings.STATICFILES_STORAGE = (
        #     'django.contrib.staticfiles.storage.ManifestStaticFilesStorage')
        settings.STATICFILES_STORAGE = (
            'barbeque.staticfiles.storage.CompactManifestStaticFilesStorage')

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
            'barbeque.staticfiles.middleware.ServeStaticFileMiddleware',
        ]
        settings.INSTALLED_APPS = settings.INSTALLED_APPS + ('django.contrib.staticfiles',)
        settings.ROOT_URLCONF = 'barbeque.tests.test_staticfiles'

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

    def test_static_folder(self, rf):
        request = rf.get('/static/doesnotexist/')
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

    @mock.patch('barbeque.staticfiles.middleware.ServeStaticFileMiddleware.process_response')
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


class TestServeStaticFileMiddlewareWithHashedFiles:

    @pytest.fixture(autouse=True)
    def setup(self, settings):
        settings.ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
        settings.STATIC_ROOT = os.path.join(settings.ROOT_DIR, 'tests', 'resources', 'static')
        settings.STATICFILES_STORAGE = (
            'django.contrib.staticfiles.storage.ManifestStaticFilesStorage')

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
            'barbeque.staticfiles.middleware.ServeStaticFileMiddleware',
        ]
        settings.INSTALLED_APPS = settings.INSTALLED_APPS + ('django.contrib.staticfiles',)
        settings.ROOT_URLCONF = 'barbeque.tests.test_staticfiles'

    def test_unhash_file_name(self):
        middleware = ServeStaticFileMiddleware()
        assert middleware.unhash_file_name(
            '/static/test_hash.11aa22bb33cc.jpg') == ('/static/test_hash.jpg')
        assert middleware.unhash_file_name('test_hash.jpg') == 'test_hash.jpg'
        assert middleware.unhash_file_name(
            'test_hash.11aa22bb33cc.11aa22bb33cc.jpg') == ('test_hash.11aa22bb33cc.jpg')
        assert middleware.unhash_file_name('test_hash.11aa22bb33cc') == 'test_hash'
        assert middleware.unhash_file_name('11aa22bb33cc') == '11aa22bb33cc'
        assert middleware.unhash_file_name('11aa22bb33cc.jpg') == '11aa22bb33cc.jpg'
        assert middleware.unhash_file_name('.11aa22bb33cc.jpg') == '.11aa22bb33cc.jpg'

    def test_hash_file_exists(self, rf):
        request = rf.get('/static/test_hash.11aa22bb33cc.jpg')
        middleware = ServeStaticFileMiddleware()
        response = middleware.process_response(request, HttpResponseNotFound(''))
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/jpeg'
        assert len(response.items()) == 3
        assert response.has_header('Content-Length')
        assert response.has_header('Last-Modified')

    def test_hash_file_original_exists(self, rf):
        request = rf.get('/static/test_hash.jpg')
        middleware = ServeStaticFileMiddleware()
        response = middleware.process_response(request, HttpResponseNotFound(''))
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/jpeg'
        assert len(response.items()) == 3
        assert response.has_header('Content-Length')
        assert response.has_header('Last-Modified')

    def test_old_hash(self, rf):
        request = rf.get('/static/test_hash.44dd55ee66ff.jpg')
        middleware = ServeStaticFileMiddleware()
        response = middleware.process_response(request, HttpResponseNotFound(''))
        assert len(response.items()) == 3
        assert response.has_header('Content-Length')
        assert response.has_header('Last-Modified')

    def test_hash_file_exists_with_client_hit(self, client, patch_settings):
        response = client.get('/static/test_hash.11aa22bb33cc.jpg')
        assert response.status_code == 200

    def test_hash_file_original_exists_with_client_hit(self, client, patch_settings):
        response = client.get('/static/test_hash.jpg')
        assert response.status_code == 200

    def test_hash_old_hash_with_client_hit(self, client, patch_settings):
        response = client.get('/static/test_hash.44dd55ee66ff.jpg')
        assert response.status_code == 200

    @mock.patch('django.contrib.staticfiles.storage.ManifestStaticFilesStorage.load_manifest')
    def test_no_staticfiles_manifest(self, manifest_mock, rf):
        manifest_mock.return_value = OrderedDict()
        request = rf.get('/static/test_hash.jpg')
        middleware = ServeStaticFileMiddleware()
        response = middleware.process_response(request, HttpResponseNotFound(''))
        assert response.status_code == 404


class TestLoadStaticfile:

    def test_invalid_path(self):
        with pytest.raises(ValueError) as exc:
            load_staticfile('foo.txt')
        assert 'not found' in force_text(exc.value)

    @mock.patch('barbeque.staticfiles.loader.open')
    def test_not_cached(self, open_mock, settings):
        open_mock.return_value.__enter__.return_value.read.return_value = 'Lorem Ipsum'
        settings.DEBUG = True
        load_staticfile._cache.clear()
        assert load_staticfile('test.txt') == 'Lorem Ipsum'
        assert open_mock.call_args[0][0].endswith('static/test.txt') is True

    @mock.patch('barbeque.staticfiles.loader.open')
    def test_cached(self, open_mock, settings):
        settings.DEBUG = True
        load_staticfile._cache.clear()
        load_staticfile._cache['test.txt'] = 'barbar'
        assert load_staticfile('test.txt') == 'barbar'
        assert open_mock.called is False


class TestCssUrlTransformer:

    def test_relative_to_absolute(self):
        assert transform_css_urls(
            'css/styles.css',
            '/web/static/css/styles.css',
            '.myclass{url("../img/logo.svg");}',
            base_url='/static/'
        ) == '.myclass{url("/static/img/logo.svg");}'

    def test_relative_to_absolute_with_schema_domain(self):
        assert transform_css_urls(
            'css/styles.css',
            '/web/static/css/styles.css',
            '.myclass{url("../img/logo.svg");}',
            base_url='http://testserver/static/'
        ) == '.myclass{url("http://testserver/static/img/logo.svg");}'

    def test_relative_to_absolute_with_schemaless_domain(self):
        assert transform_css_urls(
            'css/styles.css',
            '/web/static/css/styles.css',
            '.myclass{url("../img/logo.svg");}',
            base_url='//testserver/static/'
        ) == '.myclass{url("//testserver/static/img/logo.svg");}'

    def test_ignore_data(self):
        assert transform_css_urls(
            'css/styles.css',
            '/web/static/css/styles.css',
            '.myclass{url("data:base64,image/png:fooooooooooooo");}',
            base_url='/static/'
        ) == '.myclass{url("data:base64,image/png:fooooooooooooo");}'

    def test_ignore_absolute_schemaless(self):
        assert transform_css_urls(
            'css/styles.css',
            '/web/static/css/styles.css',
            '.myclass{url("//external/img/logo.svg");}',
            base_url='/static/'
        ) == '.myclass{url("//external/img/logo.svg");}'

    def test_ignore_absolute_schema(self):
        assert transform_css_urls(
            'css/styles.css',
            '/web/static/css/styles.css',
            '.myclass{url("http://external/img/logo.svg");}',
            base_url='/static/'
        ) == '.myclass{url("http://external/img/logo.svg");}'
