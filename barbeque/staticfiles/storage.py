from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.contrib.staticfiles.storage import ManifestFilesMixin


class CompactManifestStaticFilesStorage(ManifestStaticFilesStorage):

    def post_process(self, *args, **kwargs):
        """
        Based on django post_process from ManifestStaticFilesStorage
        """
        all_post_processed = super(ManifestFilesMixin,
                                   self).post_process(*args, **kwargs)
        for post_processed in all_post_processed:
            yield post_processed
        self.save_manifest()
        for original_file in self.hashed_files:
            self.delete(original_file)
