=======================
django-filer extensions
=======================

.. module:: barbeque.filer

.. class:: AdminFileFormField(rel, queryset, to_field_name, *args, **kwargs)

    Add additional validation capabilities for :filer:ref:`django-filer <filer:usage>`.

    :param extensions: A whitelist of extensions.
    :param alt_text_required: Validate that the ``default_alt_text`` is set.


.. class:: FilerFileField(verbose_name, *args, **kwargs)

    :filer:ref:`FilerFileField <usage>` implementation that forwards
    ``extensions`` and ``alt_text_required`` to :class:`AdminFileFormField`.
