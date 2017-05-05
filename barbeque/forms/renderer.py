from floppyforms.forms import LayoutRenderer

from .mixins import FloppyformsLayoutMixin


class FieldsetRenderer(FloppyformsLayoutMixin, LayoutRenderer):
    non_field_errors = None

    def __init__(self, form, fields=None, exclude=None, primary=False, template=None):
        assert fields or exclude is not None, 'Please provide fields or exclude argument.'

        self.form = form
        self.render_fields = fields or ()
        self.exclude_fields = exclude or ()
        self.primary_fieldset = primary

        if template:
            self.div_template_name = template

    def __str__(self):
        return self.as_div()

    @property
    def fields(self):
        visible_fields = [field.name for field in self.visible_fields()]
        return dict([
            (name, field)
            for name, field in self.form.fields.items()
            if name in visible_fields
        ])

    def hidden_fields(self):
        return self.form.hidden_fields() if self.primary_fieldset else ()

    def non_field_errors(self):
        return self.form.non_field_errors() if self.primary_fieldset else ()

    def visible_fields(self):
        form_visible_fields = self.form.visible_fields()

        if self.render_fields:
            fields = self.render_fields
        else:
            fields = [field.name for field in form_visible_fields]

        filtered_fields = [field for field in fields if field not in self.exclude_fields]

        return [field for field in form_visible_fields if field.name in filtered_fields]
