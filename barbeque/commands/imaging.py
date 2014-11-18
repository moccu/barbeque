from django.conf import settings

from .base import Command


class GmConvertCommand(Command):
    required_parameters = ['options', 'infile', 'outfile']

    command = (
        '{GM_BIN}'
        ' convert'
        ' {infile}'
        ' {options}'
        ' {outfile}'
    )

    def get_parameters(self):
        GM_BIN = getattr(settings, 'BARBEQUE_GRAPHICSMAGICK_BINARY', 'gm')
        return {
            'GM_BIN': GM_BIN,
            'infile': self.parameters['infile'],
            'outfile': self.parameters['outfile'],
            'options': ' '.join([
                '{0}{1}'.format(
                    k if k[0] == '+' else '-{0}'.format(k),
                    '' if v is True else ' {0}'.format(v)
                )
                for k, v in self.parameters['options'].items()
            ])
        }


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
