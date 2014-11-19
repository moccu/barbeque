import os
import stat
import tempfile


class MoveableNamedTemporaryFile(object):
    def __init__(self, name):
        suffix = os.path.splitext(os.path.basename(name))[1]
        self.file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)

        perms = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH

        os.chmod(self.file.name, perms)
        self.name = name

    def chunks(self):
        return self.file.read()

    def close(self):
        return self.file.close()

    def temporary_file_path(self):
        return self.file.name
