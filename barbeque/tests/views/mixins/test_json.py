from barbeque.views.mixins.json import JsonResponseMixin


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
