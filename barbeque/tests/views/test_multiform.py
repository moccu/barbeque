import pytest
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404

from barbeque.views.multiform import MultiFormView, ActionMultiFormView


class Form1(forms.Form):
    field1 = forms.CharField()
    field2 = forms.CharField()


class Form2(forms.Form):
    field1 = forms.CharField()


class MockView(MultiFormView):
    template_name = 'multiform_mockview.html'
    success_url = '/success/'
    form_classes = {
        'form1': Form1,
        'form2': Form2
    }


class TestMultiFormView:
    def test_get(self, rf):
        view = MockView.as_view()
        response = view(rf.get('/'))

        assert response.status_code == 200
        assert 'form1' in response.context_data
        assert 'form2' in response.context_data

        assert response.context_data['form1'].is_bound is False
        assert response.context_data['form2'].is_bound is False

    def test_post_invalid(self, rf):
        view = MockView.as_view()
        response = view(rf.post('/', data={'form2-field1': 'test'}))

        assert response.status_code == 200
        assert 'form1' in response.context_data
        assert 'form2' in response.context_data

        assert response.context_data['form1'].is_bound is True
        assert response.context_data['form2'].is_bound is True

        assert response.context_data['form1'].is_valid() is False
        assert response.context_data['form2'].is_valid() is True

        assert 'field1' in response.context_data['form1'].errors
        assert 'field2' in response.context_data['form1'].errors

    def test_post_valid(self, rf):
        view = MockView.as_view()
        response = view(rf.post('/', data={
            'form1-field1': 'test1',
            'form1-field2': 'test2',
            'form2-field1': 'test3'
        }))

        assert response.status_code == 302
        assert response['Location'] == '/success/'

    def test_no_success_url(self, rf):
        view = MockView.as_view(success_url=None, form_classes={'form': Form2})

        with pytest.raises(ImproperlyConfigured):
            view(rf.post('/', data={'form-field1': 'test'}))

    def test_no_form_classes(self, rf):
        view = MockView.as_view(form_classes={})

        with pytest.raises(ImproperlyConfigured):
            view(rf.get('/'))


class ActionForm1(forms.Form):
    field1 = forms.CharField()
    action = forms.CharField(initial='form1')


class ActionForm2(forms.Form):
    field2 = forms.CharField()
    action = forms.CharField(initial='form1')


class MockActionView(ActionMultiFormView):
    template_name = 'multiform_mockview.html'
    success_url = '/success/'
    form_classes = {
        'form1': ActionForm1,
        'form2': ActionForm2
    }


class TestActionMultiFormView:
    def test_get(self, rf):
        view = MockActionView.as_view()
        response = view(rf.get('/'))

        assert response.status_code == 200
        assert 'form1' in response.context_data
        assert 'form2' in response.context_data

        assert response.context_data['form1'].is_bound is False
        assert response.context_data['form2'].is_bound is False

    def test_post_invalid(self, rf):
        view = MockActionView.as_view()
        response = view(rf.post('/', data={
            'form1-action': 'form1', 'form1-field1': ''
        }))

        assert response.status_code == 200
        assert 'form1' in response.context_data
        assert 'form2' in response.context_data

        assert response.context_data['form1'].is_bound is True
        assert response.context_data['form2'].is_bound is False

        assert response.context_data['form1'].is_valid() is False

        assert 'field1' in response.context_data['form1'].errors

    def test_post_valid(self, rf):
        view = MockActionView.as_view()
        response = view(rf.post('/', data={
            'form1-action': 'form1', 'form1-field1': 'test'
        }))

        assert response.status_code == 302
        assert response['Location'] == '/success/'

    def test_no_action_in_form(self, rf):
        view = MockActionView.as_view(form_classes={'form1': Form1, 'form2': ActionForm2})

        with pytest.raises(ImproperlyConfigured):
            view(rf.get('/'))

    def test_actions_actions_in_post(self, rf):
        view = MockActionView.as_view()

        with pytest.raises(Http404):
            view(rf.post('/', data={'form1-field1': 'test'}))

    def test_multiple_actions_in_post(self, rf):
        view = MockActionView.as_view()
        with pytest.raises(Http404):
            view(rf.post(
                '/', data={'form1-action': 'form1', 'form2-action': 'form2'}))
