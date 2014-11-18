from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class ModelSearchField(forms.ModelChoiceField):
    """
    Form field to search for model instances using an `exact`/`iexact` lookup.
    By default, `pk` is used for the lookup. To change the lookup field,
    pass a `to_field_name` kwarg.
    """

    default_error_messages = {
        'invalid_choice': _('Unkown input. Please provide a valid input.')
    }

    def __init__(self, *args, **kwargs):
        self.use_iexact = kwargs.pop('use_iexact', True)
        autocomplete_url_name = kwargs.pop('autocomplete_url_name', '')
        # If we have a autocomplete_url_name, update widget attributes.
        if autocomplete_url_name:
            widget_attrs = {
                'autocomplete': 'off',
                'data-autocomplete-url': reverse_lazy(autocomplete_url_name)
            }
        else:
            widget_attrs = None
        kwargs['widget'] = kwargs.pop('widget', forms.TextInput(attrs=widget_attrs))
        super(ModelSearchField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        # No value, no lookup.
        if value in self.empty_values:
            return None

        try:
            key = self.to_field_name or 'pk'
            value = self.queryset.get(**{'{0}__{1}'.format(
                key, 'iexact' if self.use_iexact else 'exact'): value})
        except (ValueError, self.queryset.model.DoesNotExist):
            raise forms.ValidationError(
                self.error_messages['invalid_choice'], code='invalid_choice')
        return value
