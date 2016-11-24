from barbeque.filer import FilerFileField
from cms.extensions import TitleExtension
from cms.extensions.extension_pool import extension_pool
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SharingExtension(TitleExtension):
    sharing_title = models.CharField(
        _('Sharing title'), max_length=255, blank=True, null=True)

    sharing_description = models.TextField(
        _('Sharing description'), blank=True, null=True)

    sharing_image = FilerFileField(
        verbose_name=_('Sharing image'), blank=True, null=True,
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Sharing Configuration')
        verbose_name_plural = _('Sharing Configuration')

    def __str__(self):
        return str(self.extended_object)

extension_pool.register(SharingExtension)
