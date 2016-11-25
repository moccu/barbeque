from datetime import date

from django import forms

from barbeque.forms.renderer import FieldsetRenderer


class FooForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.CharField(max_length=100, required=True)
    birthdate = forms.DateField(required=True)
    secret_field = forms.CharField(widget=forms.HiddenInput)


class TestRenderer:

    def get_form(self):
        return FooForm({
            'name': 'Test',
            'email': 'foo@bar.com',
            'birthdate': date(1970, 1, 1),
            'secret_field': 'Secret',
        })

    def test_form_valid(self):
        form = self.get_form()
        valid = form.is_valid()

        assert valid is True

    def test_hidden_fields(self):
        form = self.get_form()
        renderer = FieldsetRenderer(form, exclude=(), primary=True)

        assert len(renderer.hidden_fields()) == 1

    def test_non_field_errors(self):
        form = self.get_form()
        renderer = FieldsetRenderer(form, exclude=(), primary=True)

        assert len(renderer.non_field_errors()) == 0

    def test_visible_fields(self):
        form = self.get_form()
        renderer = FieldsetRenderer(form, exclude=(), primary=True)

        assert len(renderer.visible_fields()) == len(form.fields) - 1

    def test_visible_fields_limited(self):
        form = self.get_form()
        renderer = FieldsetRenderer(form, fields=('name',), primary=True)

        assert len(renderer.visible_fields()) == 1
