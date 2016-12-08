import warnings

from .mixins import FloppyformsLayoutMixin, ItemLimitInlineMixin, PlaceholderFormMixin  # noqa


warnings.warn((
    'Importing mixins directly from barbeque.forms is deprecated and will be removed '
    'in barbeque 2.0. Use barbeque.forms.mixins instead.'
), DeprecationWarning)
