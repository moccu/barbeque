from django import template


register = template.Library()


@register.simple_tag(name='set', takes_context=True)
def set_tag(context, **kwargs):
    # We cannot use context.update - this would break the context push/pop mech.
    for key, value in kwargs.items():
        context[key] = value
    return ''
