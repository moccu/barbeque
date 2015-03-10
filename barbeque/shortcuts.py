from django.shortcuts import _get_queryset


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object, or returns None if the object doesn't exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more
    than one object is found.
    """
    queryset = _get_queryset(klass)

    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
