from subprocess import Popen, PIPE

import psutil
from django.utils import six


class CommandError(Exception):
    pass


class CommandExecutionError(CommandError):
    def __init__(self, code, stderr, command):
        message = u'code: {0} stderr: {1}'.format(code, u' '.join(stderr.split('\n')))
        super(CommandExecutionError, self).__init__(message)
        self.code = code
        self.stderr = stderr
        self.command = command


class CommandParameterError(CommandError):
    pass


class Command(object):
    pid = None
    command = 'true'
    ignore_output = True
    fail_silently = False
    required_parameters = None

    def __init__(self, **kwargs):
        self.parameters = kwargs
        if not self.validate_parameters():
            raise CommandParameterError(
                'Parameter(s) missing, required parameters: {0}'.format(
                    ', '.join(self.required_parameters)))

    def execute(self, ignore_output=None, fail_silently=None):
        command = self.get_command()
        ignore_output = ignore_output if ignore_output is not None else self.ignore_output
        fail_silently = fail_silently if fail_silently is not None else self.fail_silently

        try:
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            self.pid = process.pid

            stdout, stderr = process.communicate()
        except OSError as ex:
            raise CommandExecutionError(1, six.text_type(ex), self)

        if not fail_silently and (stderr or process.returncode != 0):
            raise CommandExecutionError(process.returncode, stderr, self)

        return True if ignore_output else self.handle_output(stdout)

    def cleanup(self):
        if self.pid is None:
            return True

        try:
            process = psutil.Process(self.pid)
            process.kill()
        except:
            pass

        return True

    def validate_parameters(self):
        return all(k in self.parameters for k in self.required_parameters or [])

    def get_parameters(self):
        return self.parameters

    def get_command(self):
        return self.command.format(**self.get_parameters()).split(' ')

    def handle_output(self, output):
        return output
