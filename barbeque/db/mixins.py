import os

from barbeque.commands.imaging import GmConvertCommand
from barbeque.utils.files import MoveableNamedTemporaryFile


class ProcessableFileMixin(object):
    process_command = GmConvertCommand

    def get_current_filename(self, field):
        return os.path.splitext(os.path.basename(field.name))

    def process_image(self, original, destination, destination_template, **kwargs):
        # Get original file parts.
        original_filename, original_extension = self.get_current_filename(original)

        # Get destination file parts.
        destination_filename = destination.field.generate_filename(
            self,
            destination_template.format(
                original=original_filename,
                extension=original_extension
            )
        )

        # Create tempfile and write image to tempfile.
        tmpfile = MoveableNamedTemporaryFile(destination_filename)
        processor = self.process_command(
            infile=original.path,
            outfile=tmpfile.temporary_file_path(),
            **kwargs
        )
        assert processor.execute()

        self.save_processed_image(tmpfile, destination, destination_filename)

        return True

    def get_storage(self, field):
        return field.storage

    def save_processed_image(self, tmpfile, destination, destination_filename):
        storage = self.get_storage(destination)

        storage.save(
            destination_filename,
            tmpfile
        )

        destination.name = destination_filename

        self.save()

    def rename_file(self, field, new_basename):
        if not field.name:
            return False

        try:
            new_filename = '{0}/{1}{2}'.format(
                os.path.dirname(field.name),
                new_basename,
                os.path.splitext(os.path.basename(field.name))[1]
            )
            os.rename(field.storage.path(field.name), field.storage.path(new_filename))
            field.name = new_filename
            self.save(update_fields=[field.field.name])
        except OSError:
            return False

        return True
