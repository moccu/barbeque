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
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class ServeStaticFileMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.path_regex = re.compile(
            r'^/{0}(.*)$'.format(settings.STATIC_URL.strip('/')))

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def serve_response(self, request, file_path):
        return serve(request, file_path, document_root=settings.STATIC_ROOT)

    def find_requested_file_hashed_name(self, requested_path):
        # Load static files mapping manifest.
        # It maps original names with hashed ones.
        storage = ManifestStaticFilesStorage()
        manifest = storage.load_manifest()
        if manifest is None or len(manifest) == 0:
            return None

        # requested file has an original (not hashed) name
        requested_path = requested_path.strip('/')
        if requested_path in manifest:
            return manifest[requested_path]

        # requested file has an old hash in name
        requested_path_parts = requested_path.split('.')
        if len(requested_path_parts) > 2 and len(requested_path_parts[-2]) == 12:
            requested_path = '{}.{}'.format(
                '.'.join(requested_path_parts[:-2]),
                requested_path_parts[-1]
            )
            if requested_path in manifest:
                return manifest[requested_path]

    def process_response(self, request, response):
        if not is_static_request(request, response):
            return response

        path = self.path_regex.match(request.path)
        if not path:
            return response

        # Try to serve a file with the same name as in the request.
        # It will work only for files which correctly hashed name,
        # as the original files without hash in name were removed from the static folder.
        try:
            return self.serve_response(request, path.group(1))
        except Http404:
            pass

        # Try to map name of a requested file with existing files.
        # We only have files with hashed names.
        requested_path = self.find_requested_file_hashed_name(path.group(1))
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
