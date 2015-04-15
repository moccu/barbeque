==================
Excel/CSV Exporter
==================

An exporter framework that allows you to export a queryset to Excel XLSX or CSV directly
from the django :class:`~django.contrib.admin.ModelAdmin` changelist view.

Example:

.. code-block:: python

    from barbeque.exporter import action_export_factory
    from django.contrib import admin

    from .models import User


    class UserAdmin(admin.ModelAdmin):
        actions = (
            action_export_factory('xlsx')
        )

        export_fields = ('id', 'first_name', 'last_name', 'street', 'city')

        actions = [
            action_export_factory('csv', 'Export as CSV', export_fields),
            action_export_factory('xlsx', 'Export as XLSX', export_fields)
        ]
