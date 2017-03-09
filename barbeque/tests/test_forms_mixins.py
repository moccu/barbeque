import mock
import pytest

import floppyforms.__future__ as floppyforms
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from barbeque.forms.mixins import (
    FloppyformsLayoutMixin, PlaceholderFormMixin, ItemLimitInlineMixin)
from barbeque.tests.resources.mockapp.models import MockModel, RelatedMockModel


class PlaceholderForm(PlaceholderFormMixin, forms.Form):
    name = forms.CharField(max_length=255, label='Name Label')

    class Meta:
        fields = '__all__'


class TestPlaceholderMixin:
    def test_attrs(self):
        form = PlaceholderForm()
        assert form.fields['name'].widget.attrs['placeholder'] == 'Name Label'


class MinInlineFormSet(ItemLimitInlineMixin, BaseInlineFormSet):
    min_items = 1


class MaxInlineFormSet(ItemLimitInlineMixin, BaseInlineFormSet):
    max_items = 2


@pytest.mark.django_db
class TestItemLimitInlineMixin:
    def setup(self):
        self.dummy_object = MockModel()
        self.dummy_object.save()
        self.dummy_related_object = RelatedMockModel(
            parent=self.dummy_object)
        self.dummy_related_object2 = RelatedMockModel(
            parent=self.dummy_object)
        self.dummy_related_object3 = RelatedMockModel(
            parent=self.dummy_object)

        self.dummy_related_object3.save()
        self.dummy_related_object2.save()
        self.dummy_related_object.save()

    def test_min_forms_valid(self):
        formset = inlineformset_factory(
            MockModel, RelatedMockModel, formset=MinInlineFormSet, fields='__all__')

        formset_instance = formset(instance=self.dummy_object, data={
            'related_mock-TOTAL_FORMS': '1',
            'related_mock-INITIAL_FORMS': '0',
            'related_mock-MAX_NUM_FORMS': '',
            'related_mock-0-parent': self.dummy_object.pk,
            'related_mock-0-id': self.dummy_related_object.pk,
        })

        assert formset_instance.is_valid() is True

    def test_min_forms_invalid(self):
        formset = inlineformset_factory(
            MockModel, RelatedMockModel, formset=MinInlineFormSet, fields='__all__')

        formset_instance = formset(instance=self.dummy_object)

        with pytest.raises(ValidationError) as exc:
            formset_instance.clean()

        assert exc.value.messages == [
            'Please provide at least 1 related mock model.']

    def test_max_forms_valid(self):
        formset = inlineformset_factory(
            MockModel, RelatedMockModel, formset=MaxInlineFormSet, extra=3, fields='__all__')

        formset_instance = formset(instance=self.dummy_object, data={
            'related_mock-TOTAL_FORMS': '2',
            'related_mock-INITIAL_FORMS': '0',
            'related_mock-MAX_NUM_FORMS': '',
            'related_mock-0-parent': self.dummy_object.pk,
            'related_mock-0-id': self.dummy_related_object.pk,
            'related_mock-1-parent': self.dummy_object.pk,
            'related_mock-1-id': self.dummy_related_object2.pk,
        })

        assert formset_instance.is_valid() is True

    def test_max_forms_invalid(self):
        formset = inlineformset_factory(
            MockModel, RelatedMockModel, formset=MaxInlineFormSet, extra=3, fields='__all__')

        formset_instance = formset(instance=self.dummy_object, data={
            'related_mock-TOTAL_FORMS': '3',
            'related_mock-INITIAL_FORMS': '0',
            'related_mock-MAX_NUM_FORMS': '',
            'related_mock-0-parent': self.dummy_object.pk,
            'related_mock-0-id': self.dummy_related_object.pk,
            'related_mock-1-parent': self.dummy_object.pk,
            'related_mock-1-id': self.dummy_related_object2.pk,
            'related_mock-2-parent': self.dummy_object.pk,
            'related_mock-2-id': self.dummy_related_object3.pk,
        })

        with pytest.raises(ValidationError) as exc:
            formset_instance.clean()

        assert exc.value.messages == [
            'Please provide at most 2 related mock models.']


class FloppyformsLayoutForm(FloppyformsLayoutMixin, floppyforms.Form):
    name = forms.CharField(max_length=255, label='Name Label')

    class Meta:
        fields = '__all__'


class TestFloppyformsLayoutMixin:

    def test_widget_type(self):
        form = FloppyformsLayoutForm()
        assert form.set_widget_types() == ''
        assert form.fields['name'].widget.widget_type == 'textinput'

    @mock.patch('barbeque.tests.test_forms_mixins.FloppyformsLayoutForm._render_as')
    def test_as_div(self, render_mock):
        FloppyformsLayoutForm().as_div()
        assert render_mock.call_args[0][0] == 'barbeque/forms/layout/div.html'
