import warnings

from .mixins import ItemLimitInlineMixin, FloppyformsLayoutMixin, PlaceholderFormMixin  # noqa


message = """Importing mixins directly from barbeque.forms is deprecated.
Use barbeque.forms.mixins instead."""

warnings.simplefilter('always', DeprecationWarning)
warnings.warn(message, DeprecationWarning)
