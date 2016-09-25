import re

from django.conf import settings
from django.http.response import Http404
from django.views.static import serve


class ServeStaticFileMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.path_regex = re.compile(
            r'^/{0}(.*)$'.format(settings.STATIC_URL.strip('/')))

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):
        if not is_static_request(request, response):
            return response
        path = self.path_regex.match(request.path)
        if not path:
            return response
        try:
            response = serve(
                request, path.group(1), document_root=settings.STATIC_ROOT)
        except Http404:
            pass
        return response


def is_static_request(request, response):
    return all([
        request.path.startswith(settings.STATIC_URL),
        response.status_code in [301, 404],
    ])
