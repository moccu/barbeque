import random
import pkg_resources

from django.contrib.messages.storage.cookie import CookieStorage
from django.http import HttpRequest
from django.utils.six.moves import xrange

import barbeque


def get_messages_from_cookie(cookies):
    request = HttpRequest()
    request.COOKIES = {CookieStorage.cookie_name: cookies.get(
        CookieStorage.cookie_name).value}
    return CookieStorage(request)


def get_random_name(min=4, max=6):
    """This function returns a pronounceable word."""
    consonants = u'bcdfghjklmnprstvwz'
    vowels = u'aeiou'
    numbers = u'0123456789'
    all = consonants + vowels

    length = random.randrange(min, (max - 2) / 2)

    def _get_name():
        return u''.join(
            random.choice(consonants) +
            random.choice(vowels) +
            random.choice(all) for x in xrange(length // 3)
        )[:length]

    name1 = _get_name()
    name2 = ''
    if random.randint(1, 2) == 1:
        name2 = _get_name() + random.choice(numbers + u'  ! ?   ')
    return '{0} {1}'.format(name1.capitalize(), name2.capitalize()).strip()


class SvgField(factory.django.FileField):

    def _make_data(self, params):
        return pkg_resources.resource_string(barbeque.__nane__, 'resources/empty.svg')
