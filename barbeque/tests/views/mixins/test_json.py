import json

from django.views.generic import FormView
from django.utils.encoding import force_text

from barbeque.tests.resources.mockapp.forms import MockForm
from barbeque.views.mixins.json import JsonResponseMixin, FormValidationJsonResponsMixin


class FormValidationView(FormValidationJsonResponsMixin, FormView):
    form_class = MockForm
    success_url = '/success/'
    template_name = 'mock.html'

form_validation_view = FormValidationView.as_view()


class TestJsonResponseMixin:
    def setup(self):
        self.mixin = JsonResponseMixin()

    def test_get_json(self):
        assert self.mixin.get_json({'test': 123}) == '{"test": 123}'

    def test_render_to_response(self):
        response = self.mixin.render_to_json({'test': 123})
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'
        assert response.content == b'{"test": 123}'


class TestFormValidationJsonResponsMixin:

    def test_invalid(self, rf):
        request = rf.post('/')
        response = form_validation_view(request)

        form = response.context_data['form']
        assert response.status_code == 200
        assert 'name' in form.errors
        assert 'text' in form.errors

    def test_invalid_json_no_fieldnames(self, rf):
        request = rf.post('/', data={'validate': True}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = form_validation_view(request)

        assert response.status_code == 200
        data = json.loads(force_text(response.content))
        assert data['errors']['missing_fields'] == 'Got no fieldname'

    def test_invalid_json(self, rf):
        data = {
            'validate': True,
            'name': '',
            'text': '',
        }
        request = rf.post('/', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = form_validation_view(request)

        assert response.status_code == 200
        data = json.loads(force_text(response.content))
        assert data['errors']['text'][0] == 'This field is required.'
        assert data['errors']['name'][0] == 'This field is required.'

    def test_valid_json(self, rf):
        data = {
            'validate': True,
            'name': 'My name',
            'text': 'My Text',
        }
        request = rf.post('/', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = form_validation_view(request)

        assert response.status_code == 200
        data = json.loads(force_text(response.content))
        assert data['errors'] is False
