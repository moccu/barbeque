from django.template import Context, Template


class TestTemplateTags:

    def test_set_tag(self):
        template = Template('{% load barbeque_tags %}{% set test_var="Some data" %}')
        context = Context()

        template.render(context)

        assert 'test_var' in context
        assert context['test_var'] == 'Some data'
