from __future__ import absolute_import

import logging
import inspect

from django.utils.six import string_types


def get_logger(obj):
    """Return a logger object with the proper module path for ``obj``."""
    # initialize settings to configure logger.
    from django.conf import settings  # noqa

    name = None
    module = getattr(inspect.getmodule(obj), '__name__', None)
    if inspect.ismethod(obj):
        name = '{module}.{cls}.{method}'.format(
            module=module,
            cls=obj.im_class.__name__,
            method=obj.__func__.__name__
        )
    elif inspect.isfunction(obj):
        name = '{module}.{function}'.format(
            module=module,
            function=getattr(obj, 'func_name', getattr(
                obj, '__qualname__', obj.__name__))
        )
    elif inspect.isclass(obj):
        name = '{module}.{cls}'.format(
            module=module,
            cls=obj.__name__
        )
    elif isinstance(obj, string_types):
        name = obj

    return logging.getLogger(name)


def logged(obj):
    """Decorator to mark a object as logged.

    This injects a ``logger`` instance into ``obj`` to make log statements
    local and correctly named.

    Example:

    .. code:: python

        >>> @logged
        ... class MyClass(object):
        ...     def foo(self):
        ...         self.logger.warning('logged')
        ...
        >>> import logging
        >>> logging.basicConfig()
        >>> obj = MyClass()
        >>> obj.foo()
        WARNING:__main__.MyClass:logged

    Supported objects:

     * Functions
     * Methods
     * Classes
     * Raw names (e.g, user at module level)

    """
    obj.logger = get_logger(obj)
    return obj


def enable_error_logging_in_debug_mode():
    """
    If DEBUG = True then monkey patch the default DEBUG 500 response, so
    that we also log the errors. (So that we can see them retrospectively).
    """
    from django.conf import settings

    if settings.DEBUG:
        from django.views import debug
        import logging

        orig_technical_500_response = debug.technical_500_response

        def custom_technical_500_response(request, exc_type, exc_value, tb):
            """
            Create a technical server error response. The last three arguments are
            the values returned from sys.exc_info() and friends.
            """
            logger = logging.getLogger('django.request')
            logger.error(
                u'Internal Server Error: %s' % request.path,
                exc_info=(exc_type, exc_value, tb),
                extra={'status_code': 500, 'request': request}
            )
            return orig_technical_500_response(request, exc_type, exc_value, tb)

        debug.technical_500_response = custom_technical_500_response
