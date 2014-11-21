from django.template import RequestContext, Template


def test_settings_context_processor(settings, rf):
    settings.THIS_IS_A_TEST = 'dude'
    settings.BARBEQUE_EXPOSED_SETTINGS = ['THIS_IS_A_TEST']
    settings.TEMPLATE_CONTEXT_PROCESSORS += ('barbeque.context_processors.settings',)

    request = rf.get('/')

    assert Template('{{ THIS_IS_A_TEST }}').render(RequestContext(request)) == 'dude'
