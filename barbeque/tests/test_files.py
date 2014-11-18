import mock

from barbeque.files import upload_to_path


class TestUtils:
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
