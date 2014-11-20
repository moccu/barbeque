import pytest

from barbeque.tests.factories.mockapp import ImageModelFactory


@pytest.mark.django_db
@pytest.mark.usefixtures('media')
class TestProcessableFileMixin:
    def setup(self):
        self.obj = ImageModelFactory.create(picture__filename='test.jpg')

    def test_get_current_filename(self):
        assert self.obj.get_current_filename(self.obj.picture) == ('test', '.jpg')
