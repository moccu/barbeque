import os

from barbeque.commands.imaging import GmConvertCommand
from barbeque.utils.files import MoveableNamedTemporaryFile


class ResizableFilerFileMixin(object):
    process_command = GmConvertCommand

    def save(self, *args, **kwargs):
        old_sha1 = self.sha1

        retval = super(ResizableFilerFileMixin, self).save(*args, **kwargs)

        if self.sha1 != old_sha1:
            self.on_file_changed()

        return retval

    def get_filename_from_field(self, field):
        return os.path.splitext(os.path.basename(field.name))

    def on_file_changed(self):
        pass

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

    def save_processed_image(self, tmpfile, destination, destination_filename):
        # Get storage and save file.
        storage = destination.storages['public' if self.is_public else 'private']
        storage.save(
            destination_filename,
            tmpfile
        )
        destination.name = destination_filename

        self.save()

    def rename_file(self, field, old_basename, new_basename):
        if not field.name:
            return False

        try:
            new_filename = '{0}/{1}{2}'.format(
                os.path.dirname(field.name),
                new_basename,
                os.path.splitext(os.path.basename(field.name))[1]
            )
            os.rename(field.path, field.storage.path(new_filename))
            field.name = new_filename
            self.save(update_fields=[field.field.name])
        except OSError:
            return False

        return True
