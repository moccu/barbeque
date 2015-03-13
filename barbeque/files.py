import os
import stat
import tempfile
import uuid

from django.template.defaultfilters import slugify


def upload_to_path(base_path, attr=None, uuid_filename=False):
    def upload_to_path_callback(instance, filename):
        if attr:
            parts = attr.split('__')
            obj_path = parts[:-1]
            field_name = parts[-1]

            obj = instance
            for part in obj_path:
                obj = getattr(obj, part)

            path = base_path % slugify(getattr(obj, field_name, '_'))
        else:
            path = base_path

        filename_parts = filename.rsplit('.', 1)

        if uuid_filename:
            filename = str(uuid.uuid4())
        else:
            filename = slugify(filename_parts[0])

        extension = len(filename_parts) > 1 and '.{0}'.format(filename_parts[-1]) or ''

        return '%s%s%s' % (path, filename, extension)

    return upload_to_path_callback


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
