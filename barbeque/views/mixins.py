from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

from django.utils.cache import (
    _generate_cache_key, add_never_cache_headers, patch_response_headers)
from django.utils.translation import ugettext

try:
    from django.core.cache import caches

    def get_cache(alias):
        return caches.get(alias)
except ImportError:
    from django.core.cache import get_cache


class LoginRequiredMixin(object):
    """
    View mixin to ensure the request is authenticated.
    Adds a message before redirecting the user.
    """
    def dispatch(self, *args, **kwargs):
        def _testfunc(user):
            if user.is_authenticated():
                return True

            messages.info(self.request, ugettext(
                'You must be logged in to access the requested page.'))
            return False

        actual_decorator = user_passes_test(
            _testfunc,
            login_url=None,
            redirect_field_name=REDIRECT_FIELD_NAME
        )

        real_dispatch = super(LoginRequiredMixin, self).dispatch
        return actual_decorator(real_dispatch)(*args, **kwargs)


class CachePageMixin(object):
    """
    View mixin to allow easy caching of view responses.
    Uses common Django cache settings like `CACHE_MIDDLEWARE_ALIAS` and
    `CACHE_MIDDLEWARE_KEY_PREFIX` for configuration.

    Also allows to cache on the server side and never caching in the client.
    To do this, set an `cache_timeout` and set `cache_ensure_never_cache` to
    True in your view class. You can pass these settings when using the
    `as_view` method.
    """

    cache_alias = settings.CACHE_MIDDLEWARE_ALIAS
    cache_key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
    cache_ensure_never_cache = False
    cache_timeout = None

    def get_page_cache_key(self, request, method='GET'):
        return _generate_cache_key(request, method, [], self.cache_key_prefix)

    def dispatch(self, request, *args, **kwargs):
        cache_key = self.get_page_cache_key(request, request.method)

        cache = get_cache(self.cache_alias)

        # Try to fetch response from cache.
        response = cache.get(cache_key, None)

        if response is None:
            # Cache not set, render response.
            response = super(CachePageMixin, self).dispatch(
                request, *args, **kwargs)

            # Apply cache headers.
            patch_response_headers(response, self.cache_timeout)

            # Override max-age if needed.
            if self.cache_ensure_never_cache:
                add_never_cache_headers(response)

            # If cache timeout is set, cache response.
            if self.cache_timeout is not None:
                # Check if we have a TemplateResponse with render method.
                if hasattr(response, 'render') and callable(response.render):
                    response.add_post_render_callback(
                        lambda r: cache.set(cache_key, r, self.cache_timeout)
                    )
                else:
                    cache.set(cache_key, response, self.cache_timeout)

        # Return response
        return response
