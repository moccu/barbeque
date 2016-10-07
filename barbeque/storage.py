import os

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class StaticFilesStorage(ManifestStaticFilesStorage):

    def url(self, name, force=False):
        """
        This implements some kind of a tricky hack to get the url for static
        files right.

        What we did is: we remove the url part "static" if it is the first part
        of the passed filenmae. The reason for this is, that we have to insert
        the "static" folder to get compass to work - compass walks through the
        path in the filesystem, the storage fail here because "static" is outside
        of our static storage. One could try to make it more generic by using
        STATIC_URL but as we hardcoded "static" everywhere, we do it here too.
        """
        name_parts = name.split(os.sep)
        if name_parts[0] == 'static':
            name = os.sep.join(name_parts[1:])

        return super().url(name, force=force)

    def post_process(self, paths, dry_run=False, **options):
        super(StaticFilesStorage, self).post_process(paths, dry_run=False, **options)
        print('XxXxXxXxXxXxX') * 10
        print(self.hashed_files)
