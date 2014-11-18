from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotAllowed


def ssl_required(view_func):
    def _checkssl(request, *args, **kwargs):
        # Only validate request if not debug and ssl enabled.
        if not settings.DEBUG and getattr(settings, 'BARBEQUE_SSL_ENABLED', True):
            # check if request is secure
            if not request.is_secure():
                # we can redirect get requests to secure url.
                if request.method == 'GET':
                    url_str = request.build_absolute_uri()
                    url_str = url_str.replace('http://', 'https://')
                    return HttpResponseRedirect(url_str)

                # all other requests are not allowed.
                return HttpResponseNotAllowed(['GET'])

        return view_func(request, *args, **kwargs)

    return _checkssl
