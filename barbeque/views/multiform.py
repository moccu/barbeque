from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic.base import TemplateResponseMixin, View


class MultiFormView(TemplateResponseMixin, View):
    form_classes = None
    success_url = None

    def get(self, request, *args, **kwargs):
        form_dict = self.get_forms()
        return self.render_to_response(self.get_context_data(**form_dict))

    def post(self, request, *args, **kwargs):
        form_dict = self.get_forms()

        valid = True
        for form in form_dict.values():
            # Only validate bound forms
            if form.is_bound and not form.is_valid():
                valid = False

        if valid:
            return self.forms_valid(form_dict)
        else:
            return self.forms_invalid(form_dict)

    def get_context_data(self, **kwargs):
        return kwargs.copy()

    def get_success_url(self):
        """Returns the supplied success URL."""
        if not self.success_url:
            raise ImproperlyConfigured(
                'No URL to redirect to. Provide a success_url.')

        # Forcing possible reverse_lazy evaluation
        return force_text(self.success_url)

    def get_form_classes(self):
        """Returns a dict with all form classes."""
        if not self.form_classes:
            raise ImproperlyConfigured(
                'No Form classes set. Provide form_classes attribute.')

        return self.form_classes.copy()

    def get_forms(self):
        """Returns a dict of initialized forms."""
        form_dict = {}
        for form_name, form_class in self.get_form_classes().items():
            kwargs = self.get_form_kwargs(form_name)
            form = form_class(**kwargs)
            form_dict[form_name] = form
        return form_dict

    def get_form_prefix(self, form_name):
        return form_name

    def get_form_kwargs(self, form_name):
        kwargs = {'prefix': self.get_form_prefix(form_name)}
        if self.request.method in ('POST', 'PUT'):
            kwargs['data'] = self.request.POST
        return kwargs

    def forms_valid(self, form_dict):
        """If forms are valid, redirect to success url."""
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form_dict):
        """Renders the template providing the forms in context."""
        return self.render_to_response(self.get_context_data(**form_dict))


class ActionMultiFormView(MultiFormView):
    action_field_name = 'action'

    def get_action(self):
        """
        Try to find an action from POST request, error if no or to many actions
        found. On all other requests, return None.
        """
        # If its not a POST request, we won't find a action, return.
        if self.request.method not in ('POST', 'PUT'):
            return None

        found_actions = []
        # Check every form for a action field using the prefix.
        for form_name in self.form_classes:
            action = self.request.POST.get(
                u'{0}-{1}'.format(
                    self.get_form_prefix(form_name),
                    self.action_field_name
                )
            )
            # If we found a action, append to our list
            if action:
                found_actions.append(action)

        # Make sure that we found exactly one action, not more, not less.
        if len(found_actions) != 1:
            raise Http404()

        return found_actions[0]

    def get_forms(self, *args, **kwargs):
        """
        Returns a dict of form instances. Ensures that every form provides an
        action field.
        """
        self.action = self.get_action()

        form_dict = super(ActionMultiFormView, self).get_forms(*args, **kwargs)
        for form in form_dict.values():
            if self.action_field_name not in form.fields:
                raise ImproperlyConfigured(
                    u'`{0}` doesn\'t provide a `{1}` field.'.format(
                        form.__class__.__name__, self.action_field_name))

        return form_dict

    def get_form_kwargs(self, form_name):
        kwargs = super(ActionMultiFormView, self).get_form_kwargs(form_name)
        if 'data' in kwargs and self.action != form_name:
            del kwargs['data']

        return kwargs

    def forms_valid(self, form_dict):
        """Subcalls to form_valid for selected form."""
        return self.form_valid(form_dict[self.action])

    def form_valid(self, form):
        """If form is valid, redirect to success url."""
        return HttpResponseRedirect(self.get_success_url())
