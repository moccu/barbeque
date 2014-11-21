import pkg_resources

import factory
from django.contrib.messages.storage.cookie import CookieStorage
from django.http import HttpRequest


def get_messages_from_cookie(cookies):
    request = HttpRequest()
    request.COOKIES = {CookieStorage.cookie_name: cookies.get(
        CookieStorage.cookie_name).value}
    return CookieStorage(request)


class SvgField(factory.django.FileField):

    def _make_data(self, params):
        return pkg_resources.resource_string(__name__, '../resources/empty.svg')
