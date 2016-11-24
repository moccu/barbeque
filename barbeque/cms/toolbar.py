from cms.cms_toolbars import (
    ADMIN_MENU_IDENTIFIER, PAGE_MENU_IDENTIFIER)
from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import SideframeItem, ModalItem, SubMenu
from django.utils.translation import ugettext_lazy as _
from .models import SharingExtension


@toolbar_pool.register
class ForceModalDialogToolbar(CMSToolbar):
    def rebuild_menu(self, menu):
        items = []
        for item in menu.items:
            if isinstance(item, SideframeItem):
                # SideframeItem appends elipsis, we need to remove them before
                # we reuse the name to avoid doubled elipsis.
                cleaned_name = item.name.rstrip(' .')
                real_item = ModalItem(
                    cleaned_name,
                    item.url,
                    active=item.active,
                    disabled=item.disabled,
                    extra_classes=item.extra_classes,
                    on_close=item.on_close,
                    side=item.side)
            elif isinstance(item, SubMenu):
                real_item = self.rebuild_menu(item)
            else:
                real_item = item

            items.append(real_item)

        menu.items = items
        return menu

    def populate(self):
        menus = [
            self.toolbar.get_menu(identifier)
            for identifier in (ADMIN_MENU_IDENTIFIER, PAGE_MENU_IDENTIFIER)
        ]

        for menu in [menu for menu in menus if menu]:
            self.rebuild_menu(menu)


@toolbar_pool.register
class SharingExtensionToolbar(ExtensionToolbar):
    model = SharingExtension
    insert_after = _('Advanced settings')

    def get_item_position(self, menu):
        for items in menu._memo.values():
            for item in items:
                if str(getattr(item, 'name', None)) in (
                    str(self.insert_after),
                    '{0}...'.format(self.insert_after)
                ):
                    return menu._item_position(item) + 1

        return None

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if not current_page_menu or not self.page:
            return

        position = self.get_item_position(current_page_menu)

        urls = self.get_title_extension_admin()
        for title_extension, url in urls:
            current_page_menu.add_modal_item(
                self.model._meta.verbose_name,
                url=url, position=position,
                disabled=not self.toolbar.edit_mode
            )
