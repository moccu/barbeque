from dateutil.relativedelta import relativedelta

from django.core.validators import BaseValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class AgeValidator(BaseValidator):
    message = _(u'You must be at least %(limit_value)d years old.')
    code = 'age'

    def compare(self, value, min_age):
        today = timezone.now()
        return value > (today - relativedelta(years=min_age)).date()


class UniqueEmailValidator(BaseValidator):
    message = _('This email address is already in use.')
    code = 'unique_email'

    def compare(self, value, qset):
        return qset.filter(email__iexact=value).exists()
