import os

import pytest

from barbeque.management.commands.create_error_pages import Command


class TestCommand:
    @pytest.fixture(autouse=True)
    def setup(self, settings):
        self.errors_dir = os.path.join(settings.STATIC_ROOT, 'errors')
        if os.path.isdir(self.errors_dir):
            for file in os.listdir(self.errors_dir):
                os.unlink(os.path.join(self.errors_dir, file))

    def test_command(self, settings):
        settings.BARBEQUE_ERRORPAGES_MAP = {'500': 'empty_template.html'}

        Command().execute()
        assert os.listdir(self.errors_dir) == ['500.html']

    def test_skip_missing_template(self, settings):
        settings.BARBEQUE_ERRORPAGES_MAP = {'500': 'empty_template.html', '503': '503.html'}

        Command().execute()
        assert os.listdir(self.errors_dir) == ['500.html']
