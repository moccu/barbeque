from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import ugettext


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
