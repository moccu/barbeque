from django.template import Context, Template

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
