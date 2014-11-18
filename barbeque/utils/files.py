import os
import tempfile


class MoveableNamedTemporaryFile(object):
    def __init__(self, name):
        suffix = os.path.splitext(os.path.basename(name))[1]
        self.file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        os.chmod(self.file.name, 0644)
        self.name = name

    def chunks(self):
        return self.file.read()

    def close(self):
        return self.file.close()

    def temporary_file_path(self):
        return self.file.name
