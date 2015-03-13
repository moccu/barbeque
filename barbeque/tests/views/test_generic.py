from barbeque.views.generic import GenericTemplateView


class TestGenericTemplateView:
    def test_get_template_names(self):
        view = GenericTemplateView()
        view.kwargs = {}

        view.kwargs['template'] = None
        assert view.get_template_names() == ['tests/index.html']

        view.kwargs['template'] = 'test123'
        assert view.get_template_names() == ['tests/test123.html']

        view.kwargs['template'] = 'abc654/test123'
        assert view.get_template_names() == ['tests/abc654/test123.html']
