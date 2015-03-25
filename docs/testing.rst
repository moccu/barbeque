===============
Testing helpers
===============

.. module:: barbeque.testing

.. function:: get_messages_from_cookie(cookies)

    Get :mod:`~django.contrib.messages` from ``cookies``

    Example:

    .. code-block:: python

        from django.test import TestCase, Client
        from barbeque.testing import get_messages_from_cookie


        class MyTest(TestCase):

            def test_error_message_on_access_denied(self):
                client = Client()

                response = client.get('/restricted/')

                assert response.status_code == 302

                messages = list(get_messages_from_cookie(response.cookies))

                assert len(messages) == 1
                assert messages[0].tags == 'error'
                assert response['Location'] == 'http://testserver/login/?next=/restricted/'
