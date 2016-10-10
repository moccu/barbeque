import os

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
# from django.contrib.staticfiles.storage import ManifestFilesMixin

from collections import OrderedDict

from django.conf import settings
from django.contrib.staticfiles.utils import matches_patterns
from django.core.files.base import ContentFile
from django.utils.encoding import force_bytes, force_text
from django.utils.six import iteritems


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

        return super(StaticFilesStorage, self).url(name, force=force)

    def post_process(self, paths, dry_run=False, **options):
        """
        post_process code copied form django HashedFilesMixin
        https://github.com/django/django/blob/master/django/contrib/staticfiles/storage.py
        Method modified to have just one copy of static file with hashed name.

        Post process the given OrderedDict of files (called from collectstatic).
        Processing is actually two separate operations:
        1. renaming files to include a hash of their content for cache-busting,
           and copying those files to the target storage.
        2. adjusting files which contain references to other files so they
           refer to the cache-busting filenames.
        If either of these are performed on a file, then that file is considered
        post-processed.
        """
        # don't even dare to process the files if we're in dry run mode
        if dry_run:
            return

        # where to store the new paths
        hashed_files = OrderedDict()

        # build a list of adjustable files
        adjustable_paths = [
            path for path in paths
            if matches_patterns(path, self._patterns.keys())
        ]

        # then sort the files by the directory level
        def path_level(name):
            return len(name.split(os.sep))

        for name in sorted(paths.keys(), key=path_level, reverse=True):

            # use the original, local file, not the copied-but-unprocessed
            # file, which might be somewhere far away, like S3
            storage, path = paths[name]
            with storage.open(path) as original_file:

                # generate the hash with the original content, even for
                # adjustable files.
                hashed_name = self.hashed_name(name, original_file)

                # then get the original's file content..
                if hasattr(original_file, 'seek'):
                    original_file.seek(0)

                hashed_file_exists = self.exists(hashed_name)
                processed = False

                # ..to apply each replacement pattern to the content
                if name in adjustable_paths:
                    content = original_file.read().decode(settings.FILE_CHARSET)
                    for extension, patterns in iteritems(self._patterns):
                        if matches_patterns(path, (extension,)):
                            for pattern, template in patterns:
                                converter = self.url_converter(name, template)
                                try:
                                    content = pattern.sub(converter, content)
                                except ValueError as exc:
                                    yield name, None, exc
                    if hashed_file_exists:
                        self.delete(hashed_name)
                    # then save the processed result
                    content_file = ContentFile(force_bytes(content))
                    saved_name = self._save(hashed_name, content_file)
                    hashed_name = force_text(self.clean_name(saved_name))
                    processed = True
                    # save file with new content
                    # delete file with original name
                    self.delete(name)
                else:
                    # or handle the case in which neither processing nor
                    # a change to the original file happened
                    if not hashed_file_exists:
                        processed = True
                        # rename original, so name contains hash
                        new_name = os.path.join(self.location, hashed_name)
                        os.rename(self.path(name), new_name)

                # and then set the cache accordingly
                hashed_files[self.hash_key(name)] = hashed_name
                yield name, hashed_name, processed

        # Finally store the processed paths
        self.hashed_files.update(hashed_files)
        self.save_manifest()

    # def post_process(self, *args, **kwargs):
    #     """
    #     Use django imlementation from ManifestStaticFilesStorage
    #     Modify it to remove files with original names
    #     """
    #     self.hashed_files = OrderedDict()
    #     all_post_processed = super(ManifestFilesMixin,
    #                                self).post_process(*args, **kwargs)
    #     for post_processed in all_post_processed:
    #         yield post_processed
    #     self.save_manifest()
    #     for original_file in self.hashed_files:
    #         self.delete(original_file)
