"""ServeStaticFileMiddleware facilitates serving static files on docker.

When serving static files with docker we first serve them through Django,
it happens only for the first time a static file is requested,
then static files are cached by nginx.

Another function of the middleware is to maps static files to their hashed names,
so it is possible to reduce static files to just files with hashed names
(without keeping the original duplicates).
"""

import re

from django.conf import settings
from django.http.response import Http404
from django.views.static import serve
from django.utils.module_loading import import_string


class ServeStaticFileMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.path_regex = re.compile(
            r'^/{0}(.*)$'.format(settings.STATIC_URL.strip('/')))
        self.manifest = self.load_staticfiles_manifest()

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def serve_response(self, request, file_path):
        return serve(request, file_path, document_root=settings.STATIC_ROOT)

    def load_staticfiles_manifest(self):
        """Staticfiles manifest maps original names to names with hash.
        The method will reise if project storage does not implement load_manifest.
        """
        storage_module = import_string(settings.STATICFILES_STORAGE)
        storage = storage_module()
        return storage.load_manifest()

    def unhash_file_name(self, requested_path):
        """Returns file original name (without hash),
        which is a key in staticfiles manifest
        """
        result = re.search(r'(.+)(\.[0-9a-f]{12})(\.?)(\w+)?$', requested_path)
        if result:
            result_str = '{}{}{}'.format(
                result.group(1) or '',
                result.group(3) or '',
                result.group(4) or ''
            )
            return result_str
        else:
            return requested_path

    def find_requested_file(self, requested_path):
        """Returns path to existing file (file path with current hash)"""
        # manifest = self.load_staticfiles_manifest()
        if self.manifest is None or len(self.manifest) == 0:
            return None

        file_name = self.unhash_file_name(requested_path).strip('/')
        try:
            return self.manifest[file_name]
        except KeyError:
            return None

    def process_response(self, request, response):
        if not is_static_request(request, response):
            return response

        path = self.path_regex.match(request.path)
        if not path:
            return response

        # Try to serve a file with original name from request
        try:
            return self.serve_response(request, path.group(1))
        except Http404:
            pass

        # Map requested file to hash and try to serve file with hash
        requested_path = self.find_requested_file(path.group(1))
        if requested_path is None:
            return response
        try:
            return self.serve_response(request, requested_path)
        except Http404:
            pass

        return response


def is_static_request(request, response):
    return all([
        request.path.startswith(settings.STATIC_URL),
        response.status_code in [301, 404],
    ])
