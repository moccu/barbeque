import os

import mock
import pytest
from compressor.exceptions import FilterError

from barbeque.compressor import UglifyJSSourcemapFilter, UglifyJSSourcemapCompressor


class TestUglifyJSSourcemapFilter:
    def test_input(self):
        assert UglifyJSSourcemapFilter(content='filter input').input() == 'filter input'

    @mock.patch('subprocess.Popen')
    def test_output(self, popen_mock, settings):
        popen_mock.return_value.wait.return_value = 0
        instance = UglifyJSSourcemapFilter(content='')

        inline_content = (
            "function test( test, test2)  { console.log(test);alert(test2 +'lorem');}")

        instance.output(root_location=settings.STATIC_ROOT, outfile='out.js', content_meta=[
            ('file', None, 'file.js'),
            ('inline', inline_content, None)
        ])

        assert popen_mock.called is True
        assert popen_mock.call_args[0][0] == (
            'uglifyjs file.js inline-68a9b9a6b48f.js -o out.js '
            '--source-map out.map.js '
            '--source-map-root /static/ '
            '--source-map-url /static/out.map.js -c -m'
        )
        assert open(os.path.join(
            settings.STATIC_ROOT, 'inline-68a9b9a6b48f.js'), 'r').read() == inline_content

    @mock.patch('subprocess.Popen')
    def test_output_popen_exception(self, popen_mock):
        popen_mock.side_effect = OSError('foo')

        instance = UglifyJSSourcemapFilter(content='')
        with pytest.raises(FilterError) as exc:
            instance.output(root_location='', outfile='out.js', content_meta=[])

        assert str(exc.value) == (
            'Unable to apply UglifyJSSourcemapFilter (uglifyjs  -o out.js '
            '--source-map out.map.js --source-map-root /static/ '
            '--source-map-url /static/out.map.js -c -m): foo'
        )

    @mock.patch('subprocess.Popen')
    def test_output_popen_errorcode(self, popen_mock):
        popen_mock.return_value.wait.return_value = 1
        popen_mock.return_value.communicate.return_value = ''

        instance = UglifyJSSourcemapFilter(content='')
        with pytest.raises(FilterError) as exc:
            instance.output(root_location='', outfile='out.js', content_meta=[])

        assert str(exc.value) == (
            'Unable to apply UglifyJSSourcemapFilter (uglifyjs  -o out.js '
            '--source-map out.map.js --source-map-root /static/ '
            '--source-map-url /static/out.map.js -c -m)'
        )

    @mock.patch('subprocess.Popen')
    def test_output_popen_error_output(self, popen_mock):
        popen_mock.return_value.wait.return_value = 1
        popen_mock.return_value.communicate.return_value = 'ERROR COMMAND OUTPUT'

        instance = UglifyJSSourcemapFilter(content='')
        with pytest.raises(FilterError) as exc:
            instance.output(root_location='', outfile='out.js', content_meta=[])

        assert str(exc.value) == 'ERROR COMMAND OUTPUT'


class TestUglifyJSSourcemapCompressor:
    @mock.patch('barbeque.compressor.UglifyJSSourcemapFilter')
    def test_output_compress_disabled(self, filter_mock, settings):
        settings.COMPRESS_ENABLED = False

        input_content = (
            "<script>function test( test, test2)  { "
            "console.log(test);alert(test2 +'lorem');}</script>"
        )

        instance = UglifyJSSourcemapCompressor(content=input_content)
        output = instance.output()
        assert filter_mock.called is False
        assert output == input_content

    @mock.patch('barbeque.compressor.UglifyJSSourcemapFilter')
    def test_output_compress_enabled(self, filter_mock, settings):
        settings.COMPRESS_ENABLED = True

        input_content = (
            "<script>function test( test, test2)  { "
            "console.log(test);alert(test2 +'lorem');}</script>"
        )

        instance = UglifyJSSourcemapCompressor(content=input_content)
        output = instance.output()
        assert filter_mock.called is True
        assert output == (
            '<script type="text/javascript" src="/static/CACHE/js/0136a2be42ec.js"></script>')

    @mock.patch('barbeque.compressor.UglifyJSSourcemapFilter')
    def test_output_compress_enabled_empty(self, filter_mock, settings):
        settings.COMPRESS_ENABLED = True

        instance = UglifyJSSourcemapCompressor(content='')
        output = instance.output()
        assert filter_mock.called is False
        assert output == ''
