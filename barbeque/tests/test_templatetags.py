import mock
import pytest
from cms.api import create_page, publish_page
import hashlib

from django.contrib.auth.models import User
from django.template import Context, Node, Template
from django.utils.text import force_text

from barbeque.staticfiles.loader import load_staticfile
from barbeque.templatetags.barbeque_tags import inline_staticfile, split, starspan, widget_type
from barbeque.tests.resources.cmsapp.models import ExtensionModel
from barbeque.tests.resources.mockapp.forms import MockForm


class TestTemplateTags:

    def test_merge_lists(self):
        first_list = [1, 2, 3]
        second_list = [4, 5, 6]
        expected_list = [1, 2, 3, 4, 5, 6]
        template = Template('{% load barbeque_tags %}{{ first_list|merge_lists:second_list }}')
        context = Context({
            'first_list': first_list,
            'second_list': second_list,
        })

        rendered = template.render(context)

        assert rendered == str(expected_list)

    def test_merge_lists_both_strings(self):
        first_list = 'foo'
        second_list = 'bar'
        expected_list = 'foo'
        template = Template('{% load barbeque_tags %}{{ first_list|merge_lists:second_list }}')
        context = Context({
            'first_list': first_list,
            'second_list': second_list,
        })

        rendered = template.render(context)

        assert rendered == expected_list

    def test_merge_lists_one_list_one_string(self):
        number_list = [1, 2, 3]
        no_list = 'bar'
        template = Template('{% load barbeque_tags %}{{ first_list|merge_lists:second_list }}')
        context = Context({
            'first_list': number_list,
            'second_list': no_list,
        })

        rendered = template.render(context)

        assert rendered == str(number_list)

        template = Template('{% load barbeque_tags %}{{ first_list|merge_lists:second_list }}')
        context = Context({
            'first_list': no_list,
            'second_list': number_list,
        })

        rendered = template.render(context)

        assert rendered == no_list

    def test_md5_string(self):
        expected = hashlib.md5('test@testing.com'.encode('utf-8')).hexdigest()
        template = Template('{% load barbeque_tags %}{{ email|md5 }}')
        context = Context({'email': 'test@testing.com'})

        rendered = template.render(context)

        assert len(rendered) == 32
        assert rendered == expected

    def test_set_tag(self):
        template = Template('{% load barbeque_tags %}{% set test_var="Some data" %}')
        context = Context()

        template.render(context)

        assert 'test_var' in context
        assert context['test_var'] == 'Some data'

    def test_split_default_sep(self):
        assert split('foo bar baz') == ['foo', 'bar', 'baz']

    def test_split_custom_sep(self):
        assert split('foo|bar baz|lorem', '|') == ['foo', 'bar baz', 'lorem']

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

    def test_widget_type_unbound(self):
        assert widget_type(MockForm().fields['name']) == 'textinput'

    def test_widget_type_bound(self):
        assert widget_type(MockForm()['name']) == 'textinput'

    def test_widget_type_custom(self):
        form = MockForm()
        form.fields['name'].widget.widget_type = 'foo'
        assert widget_type(form.fields['name']) == 'foo'


@pytest.mark.django_db
class TestPageTitleExtensionTemplateTag:

    @mock.patch('barbeque.templatetags.barbeque_tags.Page.objects.get')
    def test_no_cms(self, page_mock, activate_cms, rf):
        page_mock.side_effect = NameError
        template = Template(
            '{% load barbeque_tags %}{% page_titleextension 1 "extensionmodel" %}')
        context = Context({'request': rf.get('/')})
        with pytest.raises(ImportError):
            assert template.render(context) == ''

    def test_page_not_found(self, activate_cms, rf):
        template = Template(
            '{% load barbeque_tags %}{% page_titleextension 1 "extensionmodel" %}')
        context = Context({'request': rf.get('/')})
        assert template.render(context) == 'None'

    def test_no_page(self, activate_cms, rf):
        request = rf.get('/')
        request.user = User()
        page = create_page('Test Page', 'INHERIT', 'en-us')
        template = Template((
            '{%% load barbeque_tags %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        context = Context({'request': request})
        assert template.render(context) == 'None'

    def test_extension_not_found(self, activate_cms, rf):
        request = rf.get('/')
        request.user = User.objects.create(username='admin', is_superuser=True)

        page = create_page('Test Page', 'INHERIT', 'en-us')
        publish_page(page, request.user, 'en-us')
        page.refresh_from_db()

        template = Template((
            '{%% load barbeque_tags %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        context = Context({'request': request})
        assert template.render(context) == 'None'

    def test_extension_found_public(self, activate_cms, rf):
        request = rf.get('/')
        request.user = User.objects.create(username='admin', is_superuser=True)

        page = create_page('Test Page', 'INHERIT', 'en-us')
        publish_page(page, request.user, 'en-us')
        page.refresh_from_db()

        ExtensionModel.objects.create(
            extended_object=page.get_public_object().get_title_obj(), name='public')
        ExtensionModel.objects.create(
            extended_object=page.get_draft_object().get_title_obj(), name='draft')

        template = Template((
            '{%% load barbeque_tags %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        context = Context({'request': request})
        assert template.render(context) == 'public'

    def test_extension_found_draft(self, activate_cms, rf):
        request = rf.get('/')
        request.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        request.session = {'cms_edit': True}

        page = create_page('Test Page', 'INHERIT', 'en-us')
        publish_page(page, request.user, 'en-us')
        page.refresh_from_db()

        ExtensionModel.objects.create(
            extended_object=page.get_public_object().get_title_obj(), name='public')
        ExtensionModel.objects.create(
            extended_object=page.get_draft_object().get_title_obj(), name='draft')

        template = Template((
            '{%% load barbeque_tags %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        context = Context({'request': request})
        assert template.render(context) == 'draft'


class TestInlineStaticfileTag:

    def test_invalid_path(self):
        with pytest.raises(ValueError) as exc:
            inline_staticfile('foo.txt')
        assert 'not found' in force_text(exc.value)

    def test_valid_path(self, settings):
        settings.DEBUG = True
        load_staticfile._cache.clear()
        assert inline_staticfile('test.txt').strip() == 'Lorem Ipsum'
