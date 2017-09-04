import os

import pytest

from barbeque.management.commands.create_error_pages import Command as ErrorpagesCommand
from barbeque.management.commands.render_static_templates import Command as RenderCommand


class TestErrorpagesCommand:

    @pytest.fixture(autouse=True)
    def setup(self, settings):
        self.errors_dir = os.path.join(settings.STATIC_ROOT, 'errors')
        if os.path.isdir(self.errors_dir):
            for file in os.listdir(self.errors_dir):
                os.unlink(os.path.join(self.errors_dir, file))

    def test_command(self, settings):
        settings.BARBEQUE_ERRORPAGES_MAP = {'500': 'empty_template.html'}

        ErrorpagesCommand().execute(no_color=True)
        assert os.listdir(self.errors_dir) == ['500.html']

    def test_skip_missing_template(self, settings):
        settings.BARBEQUE_ERRORPAGES_MAP = {'500': 'empty_template.html', '503': '503.html'}

        ErrorpagesCommand().execute(no_color=True)
        assert os.listdir(self.errors_dir) == ['500.html']


class TestRenderCommand:

    def test_command(self, settings):
        settings.BARBEQUE_STATIC_TEMPLATES = {'folder/robots.txt': 'empty_template.html'}

        RenderCommand().execute(no_color=True)
        assert 'robots.txt' in os.listdir(os.path.join(settings.STATIC_ROOT, 'folder'))

    def test_skip_missing_template(self, settings):
        settings.BARBEQUE_STATIC_TEMPLATES = {
            'robots.txt': 'empty_template.html',
            'nofolder/notfound.txt': 'no_template.html',
            'folder/found.txt': 'empty_template.html',
        }

        RenderCommand().execute(no_color=True)
        assert 'robots.txt' in os.listdir(settings.STATIC_ROOT)
        assert 'found.txt' in os.listdir(os.path.join(settings.STATIC_ROOT, 'folder'))
