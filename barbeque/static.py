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

    def find_requested_file_hashed_name(self, requested_name):
        # Load static files mapping manifest.
        # It maps original names with hashed ones.
        storage = ManifestStaticFilesStorage()
        manifest = storage.load_manifest()
        if manifest is None or len(manifest) == 0:
            return None

        # requested file has an original (not hashed) name
        requested_name = requested_name.strip('/')
        if requested_name in manifest:
            return manifest[requested_name]

        # requested file has an old hash in name
        requested_name_parts = requested_name.split('.')
        if len(requested_name_parts) > 2 and len(requested_name_parts[-2]) == 12:
            requested_name = '{}.{}'.format(
                '.'.join(requested_name_parts[:-2]),
                requested_name_parts[-1]
            )
            if requested_name in manifest:
                return manifest[requested_name]

    def process_response(self, request, response):
        #  m = ManifestStaticFilesStorage()
        # import ipdb; ipdb.set_trace()
        if not is_static_request(request, response):
            return response

        path = self.path_regex.match(request.path)
        if not path:
            return response

        # Try to serve a file with the same name as in the request.
        # It will work only for files wirh corectly hashed name,
        # as the original files without hash in name were removed from the static folder.
        try:
            response = serve(
                request, path.group(1), document_root=settings.STATIC_ROOT)
            return response
        except Http404:
            pass

        # Try to map name of a requested file with existing files.
        # We only have files with hashed names.
        name = self.find_requested_file_hashed_name(path.group(1))
        if name is None:
            return response
        try:
            response = serve(
                request, name, document_root=settings.STATIC_ROOT)
        except Http404:
            pass

        return response


def is_static_request(request, response):
    return all([
        request.path.startswith(settings.STATIC_URL),
        response.status_code in [301, 404],
    ])
