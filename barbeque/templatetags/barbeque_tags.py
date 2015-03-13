from django import template


register = template.Library()


@register.simple_tag(name='set', takes_context=True)
def set_tag(context, **kwargs):
    context.update(kwargs)
    return ''
