from cms.extensions import TitleExtension
from cms.extensions.extension_pool import extension_pool
from django.db import models


class ExtensionModel(TitleExtension):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Extension'

    def __str__(self):
        return self.name

extension_pool.register(ExtensionModel)
