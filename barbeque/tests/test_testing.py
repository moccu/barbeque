from django.http import HttpResponse

from barbeque.testing import get_messages_from_cookie


def test_get_messages_from_cookie(rf):
    response = HttpResponse()
    response.set_cookie(
        'messages',
        '6e4d3a19cbcdf42bc894fc4d9ff2232200de2b40$[["__json_message",0,40,"test"]]'
    )
    messages = get_messages_from_cookie(response.cookies)
    assert len(messages) == 1
