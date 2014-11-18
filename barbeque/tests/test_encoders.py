import pytest
from django.contrib.auth import get_user_model

from barbeque.encoders import SerializableModelEncoder


class SerializableObject(object):
    def serialize(self):
        return 'test123'


@pytest.mark.django_db
class TestSerializableModelEncoder:
    def setup(self):
        self.encoder = SerializableModelEncoder()

    def test_default_serialize(self):
        assert self.encoder.default(SerializableObject()) == 'test123'

    def test_default_queryset(self):
        User = get_user_model()
        assert self.encoder.default(User.objects.all()) == list(
            User.objects.all())

    def test_default_fallback(self):
        with pytest.raises(TypeError):
            self.encoder.default(object())
