from datetime import date
from dateutil.relativedelta import relativedelta

import pytest
from django.core.exceptions import ValidationError

from barbeque.validators import AgeValidator


class TestAgeValidator:
    def setup(self):
        self.validator = AgeValidator(10)

    def test_invalid(self):
        with pytest.raises(ValidationError):
            self.validator(
                date.today() - relativedelta(years=10) + relativedelta(days=1))

    def test_valid(self):
        self.validator(date.today() - relativedelta(years=10))
