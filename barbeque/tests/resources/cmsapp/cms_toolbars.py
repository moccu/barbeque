from cms.toolbar_pool import toolbar_pool

from barbeque.cms.toolbar import TitleExtensionToolbar

from .models import ExtensionModel


class ExtensionToolbar(TitleExtensionToolbar):
    model = ExtensionModel
    insert_after = 'Advanced settings'

toolbar_pool.register(ExtensionToolbar)
