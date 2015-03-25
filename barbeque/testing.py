from django.contrib.messages.storage.cookie import CookieStorage
from django.http import HttpRequest


def get_messages_from_cookie(cookies):
    """Get :mod:`~django.contrib.messages` from ``cookies``"""
    request = HttpRequest()
    request.COOKIES = {CookieStorage.cookie_name: cookies.get(
        CookieStorage.cookie_name).value}
    return CookieStorage(request)
