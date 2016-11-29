from django import template
from django.conf import settings

try:
    from compressor.templatetags.compress import CompressorNode, OUTPUT_FILE
except ImportError:
    pass


register = template.Library()


class BuildCompressNoopNode(template.Node):

    def render(self, context):
        return ''


@register.tag
def buildcompress(parser, token):
    """
    This is a slightly duplicated version of the compressor compress tag.
    We need this tag to have a no-op output if DEBUG is True. This version
    doesn't support anything else than the "kind" option (js/css).
    """
    nodelist = parser.parse(('endbuildcompress',))
    parser.delete_first_token()
    args = token.split_contents()
    assert len(args) == 2, 'Invalid arguments to buildcompress.'

    if settings.DEBUG:
        return BuildCompressNoopNode()

    try:
        return CompressorNode(nodelist, args[1], OUTPUT_FILE, None)
    except NameError:
        raise ImportError(
            'django-compressor is required when using buildcompress tag')
