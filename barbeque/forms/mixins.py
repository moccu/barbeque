from django.core.exceptions import ValidationError
from django.utils.translation import ungettext, ugettext_lazy as _


class PlaceholderFormMixin(object):
    """
    Adds placeholder attributes to input all visible fields. The placeholder
    will be named after the field label.
    """

    def __init__(self, *args, **kwargs):
        super(PlaceholderFormMixin, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            widget = field.field.widget
            widget.attrs['placeholder'] = field.field.label


class ItemLimitInlineMixin(object):
    """Mixin that validates the min/max number of forms in an admin inline.

    Usage:

    .. code-block:: python

        class MyInlineAdmin(ItemLimitInlineMixin, admin.StackedInline):
            min_items = 1
            max_items = 4

    Please note that both options are optional and default to ``None`` thus no
    validation takes place.
    """
    min_error_message = _('Please provide at least {num} {verbose_name}.')
    max_error_message = _('Please provide at most {num} {verbose_name}.')

    min_items = None
    max_items = None

    def clean(self):
        super(ItemLimitInlineMixin, self).clean()

        forms = [
            form for form in self.forms
            if getattr(form, 'cleaned_data', {}) and not form.cleaned_data.get('DELETE', False)
        ]

        valid_forms = len([form for form in forms if form.is_valid()])

        if self.min_items and valid_forms < self.min_items:
            raise ValidationError(
                self.get_error_message(self.min_error_message, self.min_items))

        if self.max_items and valid_forms > self.max_items:
            raise ValidationError(
                self.get_error_message(self.max_error_message, self.max_items))

    def get_error_message(self, message, num):
        verbose_name = ungettext(
            self.model._meta.verbose_name,
            self.model._meta.verbose_name_plural, num)

        message = message.format(num=num, verbose_name=verbose_name)

        return message


class FloppyformsLayoutMixin(object):
    row_classname = 'form-row'
    div_template_name = 'barbeque/forms/layout/div.html'

    def set_widget_types(self):
        for name, field in self.fields.items():
            widget = self.fields[name].widget
            widget.widget_type = widget.__class__.__name__.lower()
        return ''

    def _render_as(self, *args, **kwargs):
        self.set_widget_types()
        return super()._render_as(*args, **kwargs)

    def as_div(self):
        return self._render_as(self.div_template_name)
