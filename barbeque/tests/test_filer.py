import mock
import pytest
from django import forms
from django.db import models
from filer.models import Image
from barbeque.filer import FilerFileField, AdminFileFormField

from barbeque.tests.factories.filer import ImageFactory


@pytest.mark.django_db
class TestAdminFileFormField:
    def test_super_not_clean(self):
        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id', required=False)

        assert field.clean('') is None

    def test_without_alt_text_disabled(self):
        image = ImageFactory.create(default_alt_text=None)

        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id', alt_text_required=False)
        assert isinstance(field.clean(str(image.pk)), Image)

    def test_without_alt_text_enabled(self):
        image = ImageFactory.create(default_alt_text=None)

        field = AdminFileFormField(mock.Mock(), Image.objects.all(), 'id')

        with pytest.raises(forms.ValidationError):
            field.clean(str(image.pk))

    def test_with_alt_text_enabled(self):
        image = ImageFactory.create(default_alt_text='Test')

        field = AdminFileFormField(mock.Mock(), Image.objects.all(), 'id')

        assert isinstance(field.clean(str(image.pk)), Image)

    def test_extensions_invalid_disabled(self):
        image = ImageFactory.create(default_alt_text='Test')

        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id')

        assert isinstance(field.clean(str(image.pk)), Image)

    def test_extensions_valid_enabled(self):
        image = ImageFactory.create(default_alt_text='Test')

        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id', extensions=['jpg', 'gif'])

        assert isinstance(field.clean(str(image.pk)), Image)

    def test_extensions_invalid_enabled(self):
        image = ImageFactory.create(default_alt_text='Test')

        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id', extensions=['png', 'gif'])

        with pytest.raises(forms.ValidationError):
            field.clean(str(image.pk))


class TestFilerFileField:

    def test_formfield(self):
        class FileModel(models.Model):
                file = FilerFileField()

        form_class = forms.models.modelform_factory(FileModel, fields='__all__')
        assert isinstance(form_class().fields['file'], AdminFileFormField)

    @pytest.mark.django_db
    def test_blank_null(self):
        class FileModel(models.Model):
                file1 = FilerFileField(null=True)
                file2 = FilerFileField(blank=True)
                file3 = FilerFileField()

        assert FileModel._meta.get_field('file1').blank is True
        assert FileModel._meta.get_field('file1').null is True
        assert FileModel._meta.get_field('file2').blank is True
        assert FileModel._meta.get_field('file2').null is True
        assert FileModel._meta.get_field('file3').blank is False
        assert FileModel._meta.get_field('file3').null is False
