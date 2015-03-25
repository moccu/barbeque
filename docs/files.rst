============
File helpers
============

.. module:: barbeque.files

.. function:: upload_to_path(base_path, attr=None, uuid_filename=False)

    Returns a callback suitable as ``upload_to`` argument for Django's
    :class:`~django.db.models.FileField`.

    :param base_path: Base folder structure for uploaded files. Note that
        you cannot use `strftime` placeholders here.
    :param attr: Attribute to use for base path generation.
    :param uuid_filename: Render file names as UUIDs.

    Usage:

    .. code-block:: python

        class Picture(models.Model):
            image = models.ImageField(_('Image'), upload_to=upload_to_path('uploads/images/'))

    Use ``attr`` for base path generation:

    .. code-block:: python

        class Picture(models.Model):
            image = models.ImageField(
                _('Image'),
                upload_to=upload_to_path('uploads/%s/images/', attr='category.name')
            )
            category = models.ForeignKey(Category)


.. class:: MoveableNamedTemporaryFile(name)

    Wraps :func:`~tempfile.NamedTemporaryFile` and implements `chunks`, `close`
    and `temporary_file_path` on top of it.

    Suitable for the django storage system to allow files to simply get moved to it's final
    location instead of copying the file-contents.
