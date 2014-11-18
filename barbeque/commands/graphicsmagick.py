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
