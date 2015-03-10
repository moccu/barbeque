from __future__ import absolute_import

import logging
import inspect

from django.utils.six import string_types

from barbeque.compat import PY3


def _get_class_name(obj):
    if not PY3:
        return obj.im_class.__name__
    return obj.__self__.__class__.__name__


def get_logger(obj):
    """Return a logger object with the proper module path for ``obj``."""
    # initialize settings to configure logger.
    from django.conf import settings  # noqa

    name = None
    module = getattr(inspect.getmodule(obj), '__name__', None)
    if inspect.ismethod(obj):
        name = '{module}.{cls}.{method}'.format(
            module=module,
            cls=_get_class_name(obj),
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
