import sys

from django.db import router, transaction, IntegrityError, DatabaseError
from django.shortcuts import _get_queryset
from django.utils import six


def create_or_update(model, using=None, **kwargs):
    """
    Similar to get_or_create, either updates a row or creates it.

    The result will be (rows affected, False), if the row was not created,
    or (instance, True) if the object is new.

    >>> create_or_update(MyModel, key='value', defaults={
    >>>     'value': F('value') + 1,
    >>> })
    """
    assert kwargs, 'create_or_update must be passed at least one keyword argument'

    defaults = kwargs.pop('defaults', {})
    lookup = kwargs.copy()
    for f in model._meta.fields:
        if f.attname in lookup:
            lookup[f.name] = lookup.pop(f.attname)

    params = dict([(k, v) for k, v in kwargs.items() if '__' not in k])
    params.update(defaults)

    if not using:
        using = router.db_for_write(model)

    # Correctly select database routing and select the database for writing.
    # This is also important if proxies for pooling in use.
    qset = model.objects.using(using)
    exists = qset.filter(**lookup).exists()
    if exists:
        qset.filter(**lookup).update(**params)
    else:
        try:
            obj = model(**params)
            with transaction.atomic(using=using):
                obj.save(force_insert=True, using=using)
        except (IntegrityError, DatabaseError):
            exc_info = sys.exc_info()
            try:
                qset.filter(**lookup).update(**params)
            except IntegrityError:
                # Re-raise the IntegrityError with its original traceback.
                six.reraise(*exc_info)


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
