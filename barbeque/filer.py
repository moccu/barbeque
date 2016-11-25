from __future__ import absolute_import

import os

from django import forms
from django.utils.translation import ugettext
from filer.fields.file import (
    AdminFileFormField as BaseAdminFileFormField, FilerFileField as BaseFilerFileField)


class AdminFileFormField(BaseAdminFileFormField):
    def __init__(self, *args, **kwargs):
        self.extensions = kwargs.pop('extensions', None)
        self.alt_text_required = kwargs.pop('alt_text_required', True)
        super(AdminFileFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        cleaned = super(AdminFileFormField, self).clean(value)

        if not cleaned:
            return cleaned

        if self.extensions:
            extension = os.path.splitext(cleaned.file.name)[1].strip('.').lower()
            if extension not in self.extensions:
                raise forms.ValidationError(
                    ugettext('Invalid file extension, allowed extensions: {0}'.format(
                        ', '.join(self.extensions))))

        if self.alt_text_required:
            if hasattr(cleaned, 'default_alt_text') and not cleaned.default_alt_text:
                raise forms.ValidationError(
                    ugettext('Alternative text is missing for this file.'))

        return cleaned


class FilerFileField(BaseFilerFileField):
    default_form_class = AdminFileFormField

    def __init__(self, verbose_name=None, *args, **kwargs):
        kwargs['verbose_name'] = verbose_name
        if 'related_name' not in kwargs:
            kwargs['related_name'] = '+'
        if kwargs.pop('blank', False) or kwargs.pop('null', False):
            kwargs['null'] = True
            kwargs['blank'] = True

        self.extensions = kwargs.pop('extensions', None)
        self.alt_text_required = kwargs.pop('alt_text_required', True)

        super(FilerFileField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'extensions': self.extensions,
            'alt_text_required': self.alt_text_required,
        }
        defaults.update(kwargs)
        return super(FilerFileField, self).formfield(**defaults)
