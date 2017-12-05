from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage


def load_staticfile(name, postprocessor=None):
    if not hasattr(load_staticfile, '_cache'):
        load_staticfile._cache = {}

    if name in load_staticfile._cache:
        return load_staticfile._cache[name]

    if settings.DEBUG:
        # Dont access file via staticfile storage in debug mode. Not available
        # without collectstatic management command.
        path = find(name)
    elif staticfiles_storage.exists(name):
        # get path if target file exists.
        path = staticfiles_storage.path(name)
    else:
        path = None

    if not path:
        raise ValueError('Staticfile not found for inlining: {0}'.format(name))

    with open(path, 'r') as staticfile:
        content = staticfile.read()

    if postprocessor:
        content = postprocessor(name, path, content)

    if not settings.DEBUG:
        load_staticfile._cache[name] = content

    return content

load_staticfile._cache = {}
