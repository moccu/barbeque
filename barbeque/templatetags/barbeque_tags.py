import re

from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

try:
    from cms.models import Page
    from cms.utils.moderator import use_draft
except ImportError:
    pass

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


@register.simple_tag
def hashed_staticfile(path):
    try:
        return staticfiles_storage.hashed_name(path)
    except (AttributeError, ValueError):
        return path


@register.simple_tag(takes_context=True)
def page_titleextension(context, page_id, extension):
    try:
        page = Page.objects.get(pk=page_id)
        if 'request' in context and use_draft(context['request']):
            page = page.get_draft_object()
        else:
            page = page.get_public_object()
    except NameError:
        raise ImportError(
            'django-cms is required when using page_titleextension tag')
    except Page.DoesNotExist:
        return None

    if not page:
        return None

    try:
        return getattr(page.get_title_obj(), extension)
    except ObjectDoesNotExist:
        return None


@register.filter
def widget_type(field):
    # Check if field is bound field.
    if all(hasattr(field, attr) for attr in ('as_widget', 'as_hidden', 'is_hidden')):
        field = field.field

    return getattr(
        field.widget,
        'widget_type',
        field.widget.__class__.__name__.lower()
    )
