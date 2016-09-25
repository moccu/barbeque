import os
import mock

import pytest
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect

from barbeque.static import ServeStaticFileMiddleware


@pytest.fixture
def patch_settings(settings):
    settings.ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    settings.STATIC_ROOT = os.path.join(settings.ROOT_DIR, 'tests', 'resources', 'static')


def test_file_exists(rf, db, patch_settings):
    request = rf.get('/static/test.jpg')
    middleware = ServeStaticFileMiddleware()
    response = middleware.process_response(request, HttpResponseNotFound(''))
    assert response.status_code == 200
    assert response['Content-Type'] == 'image/jpeg'
    assert len(response.items()) == 3
    assert response.has_header('Content-Length')
    assert response.has_header('Last-Modified')


def test_file_missing(rf, patch_settings):
    request = rf.get('/static/doesnotexist.jpg')
    middleware = ServeStaticFileMiddleware()
    response = middleware.process_response(request, HttpResponseNotFound(''))
    assert response.status_code == 404


def test_unknown_prefix(rf, patch_settings):
    request = rf.get('/foo/test.jpg')
    middleware = ServeStaticFileMiddleware()
    response = middleware.process_response(request, HttpResponseNotFound(''))
    assert response.status_code == 404


def test_redirect_for_static(rf, db, patch_settings):
    request = rf.get('/static/test.jpg')
    middleware = ServeStaticFileMiddleware()
    response = middleware.process_response(
        request, HttpResponsePermanentRedirect('/static/test.jpg/'))
    assert response.status_code == 200


def test_redirect_other(rf, db, patch_settings):
    request = rf.get('/foo')
    middleware = ServeStaticFileMiddleware()
    redirect = HttpResponsePermanentRedirect('/foo/')
    response = middleware.process_response(request, redirect)
    assert response == redirect


@mock.patch('barbeque.static.ServeStaticFileMiddleware.process_response')
def test_new_style_middleware(process_response_mock, rf, patch_settings):
    request = rf.get('/static/test.jpg')
    get_response_mock = mock.Mock()
    get_response_mock.return_value = HttpResponseNotFound()
    middleware = ServeStaticFileMiddleware(get_response=get_response_mock)
    middleware(request)
    get_response_mock.assert_called_with(request)
    process_response_mock.assert_called_with(
        request, get_response_mock.return_value)


# Examples of application tests:

# def test_with_client_hit(client, db, patch_settings):
#     response = client.get('/static/test.jpg')
#     assert response.status_code == 200


# def test_with_client_redirect(client, db, patch_settings):
#     response = client.get('/foo')
#     assert response.status_code == 301
#     assert response['Location'] == '/foo/'


# def test_with_client_query_params(client, db, patch_settings):
#     response = client.get('/static/test.jpg?v=1')
#     assert response.status_code == 200
#     assert response['Content-Type'] == 'image/jpeg'
