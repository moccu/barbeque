import os
import stat
import tempfile
import uuid

from django.template.defaultfilters import slugify
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text


@deconstructible
class UploadToPath(object):

    def __init__(self, base_path, attr=None, uuid_filename=False):
        self.base_path = base_path
        self.attr = attr
        self.uuid_filename = uuid_filename

    def __call__(self, instance, filename):
        if self.attr:
            parts = self.attr.split('__')
            obj_path = parts[:-1]
            field_name = parts[-1]

            obj = instance
            for part in obj_path:
                obj = getattr(obj, part)

            path = self.base_path % slugify(getattr(obj, field_name, '_'))
        else:
            path = self.base_path

        filename_parts = filename.rsplit('.', 1)

        if self.uuid_filename:
            filename = force_text(uuid.uuid4())
        else:
            filename = slugify(filename_parts[0])

        extension = len(filename_parts) > 1 and u'.{0}'.format(filename_parts[-1]) or ''

        return os.path.join(path, u'{0}{1}'.format(filename, extension))


def upload_to_path(base_path, attr=None, uuid_filename=False):
    return UploadToPath(base_path, attr=attr, uuid_filename=uuid_filename)


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
