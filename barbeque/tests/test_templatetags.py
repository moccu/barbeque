import mock
from django.template import Context, Node, Template

from barbeque.templatetags.barbeque_tags import starspan


class TestTemplateTags:

    def test_set_tag(self):
        template = Template('{% load barbeque_tags %}{% set test_var="Some data" %}')
        context = Context()

        template.render(context)

        assert 'test_var' in context
        assert context['test_var'] == 'Some data'

    def test_starspan_no_blocks(self):
        assert starspan('test * **foo bar*** lorem') == (
            'test * **foo bar*** lorem')

    def test_starspan_multiple_blocks(self):
        assert starspan('***asd foo** bar*** lorem ipsum *** dolor sit***') == (
            '<span>asd foo** bar</span> lorem ipsum <span> dolor sit</span>')

    def test_starspan_unbalanced_blocks(self):
        assert starspan('asd foo** bar*** lorem ipsum *** dolor sit***') == (
            'asd foo** bar<span> lorem ipsum </span> dolor sit***')

    @mock.patch('barbeque.templatetags.buildcompress.CompressorNode')
    def test_buildcompress_tag_debug(self, node_mock, settings):
        settings.DEBUG = True
        node_mock.return_value = Node()

        template = Template(
            '{% load buildcompress %}{% buildcompress "css" %}foo{% endbuildcompress %}')
        template.render(Context())

        assert node_mock.called is False

    @mock.patch('barbeque.templatetags.buildcompress.CompressorNode')
    def test_buildcompress_tag_no_debug(self, node_mock, settings):
        settings.DEBUG = False
        node_mock.return_value = Node()

        template = Template(
            '{% load buildcompress %}{% buildcompress "css" %}foo{% endbuildcompress %}')
        template.render(Context())

        assert node_mock.called is True
