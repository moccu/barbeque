import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()


STARSPAN_RE = re.compile(r'(\*\*\*)(.+?)\1')


@register.simple_tag(name='set', takes_context=True)
def set_tag(context, **kwargs):
    # We cannot use context.update - this would break the context push/pop mech.
    for key, value in kwargs.items():
        context[key] = value
    return ''


@register.filter
@stringfilter
def starspan(value):
    return mark_safe(STARSPAN_RE.sub(r'<span>\2</span>', conditional_escape(value)))
