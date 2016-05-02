from cms.cms_toolbars import (
    ADMIN_MENU_IDENTIFIER, PAGE_MENU_IDENTIFIER)
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import SideframeItem, ModalItem, SubMenu


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

toolbar_pool.register(ForceModalDialogToolbar)
