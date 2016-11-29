import mock
from cms.api import create_page
from cms.toolbar.items import ModalItem, SideframeItem


def test_forcemodaldialogtoolbar(admin_client, activate_cms):
    page = create_page('Test Page', 'INHERIT', 'en-us')

    response = admin_client.get('{0}?edit=on'.format(page.get_absolute_url()))
    toolbar = response.context['request'].toolbar
    for item in toolbar.get_menu('admin-menu').items:
        assert item.__class__ is not SideframeItem


def test_titleextensiontoolbar_inserted(admin_client, activate_cms):
    page = create_page('Test Page', 'INHERIT', 'en-us')

    response = admin_client.get('{0}?edit=on'.format(page.get_absolute_url()))
    toolbar = response.context['request'].toolbar
    menu = toolbar.get_menu('page')
    item = menu.items[5]
    assert isinstance(item, ModalItem)
    assert item.name == 'Extension...'
    assert item.url.startswith('/admin/cmsapp/extensionmodel/')


@mock.patch('barbeque.cms.toolbar.TitleExtensionToolbar.get_item_position')
def test_titleextensiontoolbar_not_inserted(position_mock, admin_client, activate_cms):
    response = admin_client.get('/non-cms/')
    toolbar = response.context['request'].toolbar
    assert toolbar.get_menu('page') is None
    assert position_mock.called is False
