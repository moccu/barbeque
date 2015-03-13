from django.conf import settings as django_settings


def settings(request):
    parameters = getattr(django_settings, 'BARBEQUE_EXPOSED_SETTINGS', ['DEBUG'])

    context = {}
    for parameter in parameters:
        context[parameter] = getattr(django_settings, parameter, None)

    return context
