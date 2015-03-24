=========
Shortcuts
=========

.. module:: barbeque.shortcuts

.. function:: get_object_or_none(klass, *args, **kwargs):

Uses :meth:`~django.db.models.query.QuerySet.get()` to return an object, or returns ``None`` if the object doesn't exist.

``klass`` may be a :class:`~django.db.models.Model`, :class:`~django.db.models.Manager`,
or :class:`~django.db.models.query.QuerySet` object. All other passed arguments and
keyword arguments are used in the :meth:`~django.db.models.query.QuerySet.get()` query.

Note: Like with :meth:`~django.db.models.query.QuerySet.get()`,
a :exc:`~django.core.exceptions.MultipleObjectsReturned` will be raised if
more than one object is found.
