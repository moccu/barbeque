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


class ServeStaticFileMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.path_regex = re.compile(
            r'^/{0}(.*)$'.format(settings.STATIC_URL.strip('/')))
        try:
            self.manifest = self.load_staticfiles_manifest()
        except AttributeError:
            self.manifest = None

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def serve_response(self, request, file_path):
        return serve(request, file_path, document_root=settings.STATIC_ROOT)

    def load_staticfiles_manifest(self):
        """Staticfiles manifest maps original names to names with hash.
        The method will reise if project storage does not implement load_manifest.
        """
        storage_path, storage_class = settings.STATICFILES_STORAGE.rsplit('.', 1)
        exec('from {} import {}'.format(storage_path, storage_class))
        storage = eval('{}()'.format(storage_class))
        return storage.load_manifest()

    def unhash_file_name(self, requested_path):
        """Returns file original name (without hash),
        which is a key in staticfiles manifest
        """
        temp_path = re.sub(r'(\.[0-9a-f]{12})\.?(\w+)$', r'.\2', requested_path)
        return re.sub(r'(\.[0-9a-f]{12})$', r'', temp_path)

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

        # Try to serve a file from request
        try:
            return self.serve_response(request, path.group(1))
        except Http404:
            pass

        # Map requested file to hash.
        # We only have files with hashed names.
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
