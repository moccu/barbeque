import pytest
import mock
from django.core.exceptions import MultipleObjectsReturned
from django.db.utils import ConnectionDoesNotExist

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

    @mock.patch('barbeque.db.shortcuts.router.db_for_write')
    def test_using_defaults_to_write_db(self, db_for_write):
        db_for_write.return_value = 'default'

        create_or_update(DummyModel, name='Dummy', slug='dummy')
        db_for_write.assert_called_once_with(DummyModel)

    def test_forwards_using(self):
        with pytest.raises(ConnectionDoesNotExist) as excinfo:
            create_or_update(DummyModel, using='write', name='Dummy', slug='dummy')

        assert "The connection write doesn't exist" in str(excinfo)

    def test_handle_integrity_error(self):
        # Catch database error, not-matching filter
        create_or_update(DummyModel, name=None)

        assert DummyModel.objects.count() == 0

        # Catch integrity error
        create_or_update(DummyModel, name='dummy', slug='dummy')
        create_or_update(DummyModel, name='dummy 2', slug='dummy')

    def test_require_filter(self):
        with pytest.raises(AssertionError):
            create_or_update(DummyModel)


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
