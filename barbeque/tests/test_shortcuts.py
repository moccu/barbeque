import pytest
from django.core.exceptions import MultipleObjectsReturned

from barbeque.shortcuts import get_object_or_none
from barbeque.tests.resources.mockapp.models import DummyModel


@pytest.mark.django_db
class TestGetObjectOrNone:

    def test_get_none_on_not_exist(self):
        assert get_object_or_none(DummyModel) is None

    def test_get_object(self):
        obj = DummyModel.objects.create(name='Dummy', slug='dummy')

        assert get_object_or_none(DummyModel) == obj

    def test_get_object_filter(self):
        DummyModel.objects.create(name='Dummy', slug='dummy')
        obj = DummyModel.objects.create(name='Dummy2', slug='dummy2')

        assert get_object_or_none(DummyModel, slug='dummy2') == obj

    def test_only_catches_does_not_exist(self):
        DummyModel.objects.create(name='Dummy', slug='dummy')
        DummyModel.objects.create(name='Dummy2', slug='dummy2')

        with pytest.raises(MultipleObjectsReturned):
            get_object_or_none(DummyModel)
