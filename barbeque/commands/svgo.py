from django.conf import settings

from .base import Command


class SvgoCommand(Command):
    required_parameters = ['infile', 'outfile']

    command = (
        '{SVGO_BIN}'
        ' -i {infile}'
        ' -o {outfile}'
    )

    def get_parameters(self):
        SVGO_BIN = getattr(settings, 'BARBEQUE_SVGO_BINARY', 'svgo')
        return {
            'SVGO_BIN': SVGO_BIN,
            'infile': self.parameters['infile'],
            'outfile': self.parameters['outfile'],
        }
