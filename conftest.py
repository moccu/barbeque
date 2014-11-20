import shutil
import tempfile

import pytest


@pytest.yield_fixture()
def media(request, settings):
    tmpdir = tempfile.mkdtemp()
    settings.MEDIA_ROOT = tmpdir
    yield
    shutil.rmtree(tmpdir)
