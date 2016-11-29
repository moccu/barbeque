from datetime import date
from dateutil.relativedelta import relativedelta

import pytest
from django.core.exceptions import ValidationError

from barbeque.validators import AgeValidator, UniqueEmailValidator
from barbeque.tests.resources.mockapp.models import DummyModel


class TestAgeValidator:
    def setup(self):
        self.validator = AgeValidator(10)

    def test_invalid(self):
        with pytest.raises(ValidationError):
            self.validator(
                date.today() - relativedelta(years=10) + relativedelta(days=1))

    def test_valid(self):
        self.validator(date.today() - relativedelta(years=10))


@pytest.mark.django_db
class TestEmailValidator:

    def test_unique(self):
        UniqueEmailValidator(DummyModel.objects.all())('foo@bar.baz')

    def test_not_unique(self):
        DummyModel.objects.create(name='foo', slug='bar', email='foo@bar.baz')

        with pytest.raises(ValidationError):
            UniqueEmailValidator(DummyModel.objects.all())('foo@bar.baz')

    def test_not_unique_uppercase(self):
        DummyModel.objects.create(name='foo', slug='bar', email='foo@bar.baz')

        with pytest.raises(ValidationError):
            UniqueEmailValidator(DummyModel.objects.all())('FOO@BAR.baz')
