import os

import mock
from django.utils.encoding import force_bytes

from barbeque.files import upload_to_path, MoveableNamedTemporaryFile


class TestUploadToPath:
    def test_upload_to_path_with_attr(self):
        instance = mock.Mock()
        instance.testattr.testattr2.test123 = 'test'
        cb = upload_to_path('folder/%s/sub/', 'testattr__testattr2__test123')

        assert cb(instance, 'testfile.ext') == 'folder/test/sub/testfile.ext'

    def test_upload_to_path_without_attr(self):
        instance = mock.Mock()
        cb = upload_to_path('folder/sub/')

        assert cb(instance, 'testfile.ext') == 'folder/sub/testfile.ext'

    def test_upload_to_path_with_uuid(self):
        instance = mock.Mock()
        cb = upload_to_path('folder/sub/', uuid_filename=True)

        with mock.patch('uuid.uuid4') as m:
            m.return_value = 'foobar'
            assert cb(instance, 'testfile.ext') == 'folder/sub/foobar.ext'


class TestMoveableNamedTemporaryFile:
    def test_init(self):
        tmp = MoveableNamedTemporaryFile('test.jpg')

        assert tmp.name == 'test.jpg'

        # Ensure file rights are set
        assert os.stat(tmp.file.name).st_mode == 33188

    def test_chunks(self):
        tmp = MoveableNamedTemporaryFile('test.jpg')
        tmp.file.write(force_bytes('test123'))
        tmp.file.seek(0)
        assert tmp.chunks() == force_bytes('test123')

    def test_close(self):
        tmp = MoveableNamedTemporaryFile('test.jpg')
        tmp.close()
        assert tmp.file.file.closed is True

    def test_temporary_file_path(self):
        tmp = MoveableNamedTemporaryFile('test.jpg')
        assert tmp.temporary_file_path() == tmp.file.name
        assert tmp.temporary_file_path().endswith('.jpg') is True
