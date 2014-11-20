import pytest
from PIL import Image

from barbeque.tests.factories.mockapp import ImageModelFactory


@pytest.mark.django_db
@pytest.mark.usefixtures('media')
class TestProcessableFileMixin:
    def setup(self):
        self.obj = ImageModelFactory.create()

    def test_get_current_filename(self):
        assert self.obj.get_current_filename(self.obj.picture) == ('test', '.jpg')

    def test_process_image(self):
        assert self.obj.process_image(
            self.obj.picture, self.obj.resized, '{original}_200{extension}',
            options={'resize': '200x'})

        assert self.obj.resized is not None

        resized = Image.open(self.obj.resized.path)

        assert resized.size == (200, 200)

    def test_get_storage(self):
        assert self.obj.get_storage(self.obj.picture) == self.obj.picture.storage

    def test_rename_file_no_filename(self):
        assert not self.obj.rename_file(self.obj.resized, 'dada', 'dadada')
