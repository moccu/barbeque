from django.conf import settings as dj_settings


def settings(request):
    parameters = getattr(dj_settings, 'BARBEQUE_EXPOSED_SETTINGS', ['DEBUG'])

    context = {}
    for parameter in parameters:
        context[parameter] = getattr(dj_settings, parameter, None)

    return context
