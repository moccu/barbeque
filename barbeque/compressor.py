from __future__ import absolute_import

import os
import subprocess

from compressor.cache import get_hexdigest
from compressor.conf import settings
from compressor.exceptions import FilterError
from compressor.filters import CompilerFilter
from compressor.js import JsCompressor
from django.utils.safestring import mark_safe


class UglifyJSFilter(CompilerFilter):
    command = '{binary} {args}'
    options = (
        ('binary', getattr(settings, 'COMPRESS_UGLIFYJS_BINARY', 'uglifyjs')),
        ('args', getattr(settings, 'COMPRESS_UGLIFYJS_ARGUMENTS', '-')),
    )


class UglifyJSSourcemapFilter(CompilerFilter):
    command = (
        u'{binary}'
        u' {infiles}'
        u' -o {outfile}'
        u' --source-map {mapfile}'
        u' --source-map-root {maproot}'
        u' --source-map-url {maproot}{mapfile}'
        u' -c -m'
    )
    options = (
        ('binary', getattr(settings, 'COMPRESS_UGLIFYJS_BINARY', 'uglifyjs')),
    )

    def input(self, **kwargs):
        return self.content

    def output(self, **kwargs):
        self.cwd = kwargs['root_location']

        infiles = []
        tmpinfiles = []
        inline_base_dir = os.path.join(self.cwd, os.path.dirname(kwargs['outfile']))

        for infile in kwargs['content_meta']:
            filename = infile[2]
            if filename is None and infile[0] == 'inline':
                inline_content = infile[1].encode(self.default_encoding)
                inline_path = os.path.join(
                    inline_base_dir,
                    'inline-{0}.js'.format(get_hexdigest(inline_content, 12))
                )
                tmpinfile = open(inline_path, 'wb')
                tmpinfile.write(inline_content)
                tmpinfile.flush()
                tmpinfiles.append(tmpinfile)

                filename = os.path.relpath(tmpinfile.name, self.cwd)

            infiles.append(filename)

        options = dict(self.options)
        options['infiles'] = ' '.join(f for f in infiles)
        options['outfile'] = kwargs['outfile']
        options['mapfile'] = kwargs['outfile'].replace('.js', '.map.js')
        options['maproot'] = settings.STATIC_URL

        try:
            command = self.command.format(**options)

            proc = subprocess.Popen(
                command, shell=True, cwd=self.cwd,
                stdout=self.stdout, stdin=self.stdin, stderr=self.stderr
            )
            err = proc.communicate()
        except (IOError, OSError) as e:
            raise FilterError('Unable to apply {0} ({1}): {2}'.format(
                self.__class__.__name__, command, e))
        else:
            if proc.wait() != 0:
                if not err:
                    err = 'Unable to apply {0} ({1})'.format(
                        self.__class__.__name__, command)
                raise FilterError(err)
        finally:
            for tmpinfile in tmpinfiles:
                tmpinfile.close()


class UglifyJSSourcemapCompressor(JsCompressor):

    def output(self, mode='file', forced=False):
        """
        The general output method, override in subclass if you need to do
        any custom modification. Calls other more specific methods or simply
        returns the content directly.
        """
        content = self.filter_input(forced)
        if not content:
            return ''

        concatenated_content = '\n'.join(self.filter_input(forced))

        if settings.COMPRESS_ENABLED or forced:
            output_filepath = self.get_filepath(concatenated_content, basename=None)

            UglifyJSSourcemapFilter(content).output(
                outfile=output_filepath,
                content_meta=self.split_content,
                root_location=self.storage.base_location
            )

            return self.output_file(mode, output_filepath)

        return concatenated_content

    def output_file(self, mode, new_filepath):
        url = mark_safe(self.storage.url(new_filepath))
        return self.render_output(mode, {'url': url})
