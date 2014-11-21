import pytest

from barbeque.db.shortcuts import create_or_update

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
