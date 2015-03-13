from cms.api import create_page
from cms.toolbar.items import SideframeItem


def test_forcemodaldialogtoolbar(admin_client, activate_cms):
    page = create_page('Test Page', 'INHERIT', 'en-us')

    response = admin_client.get('{0}?edit=on'.format(page.get_absolute_url()))
    toolbar = response.context['request'].toolbar
    for item in toolbar.get_menu('admin-menu').items:
        assert item.__class__ is not SideframeItem
