import pytest
from django.core.exceptions import MultipleObjectsReturned

from barbeque.db.shortcuts import create_or_update, get_object_or_none

from barbeque.tests.resources.mockapp.models import DummyModel


@pytest.mark.django_db
class TestCreateOrUpdateHelper:

    def test_create_or_update_create(self):
        assert DummyModel.objects.count() == 0
        create_or_update(DummyModel, name='Dummy', slug='dummy')
        dummy = DummyModel.objects.get()
        assert dummy.name == 'Dummy'
        assert dummy.slug == 'dummy'

    def test_create_or_update_update(self):
        assert DummyModel.objects.count() == 0

        create_or_update(DummyModel, slug='dummy', defaults={'name': 'Dummy'})
        create_or_update(DummyModel, slug='dummy', defaults={'name': 'Dummy'})

        dummy = DummyModel.objects.get()
        assert dummy.name == 'Dummy'

        create_or_update(DummyModel, slug='dummy', defaults={'name': 'New Dummy'})

        dummy = DummyModel.objects.get()
        assert dummy.name == 'New Dummy'


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
