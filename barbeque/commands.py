import psutil
try:
    from gevent.subprocess import Popen, PIPE
except ImportError:
    from subprocess import Popen, PIPE


class CommandError(Exception):
    pass


class CommandExecutionError(CommandError):
    def __init__(self, message, code, command):
        Exception.__init__(self, message)
        self.code = code
        self.command = command


class CommandParameterError(CommandError):
    pass


class Command(object):
    pid = None
    command = 'true'
    output = False
    fail_silently = False
    required_parameters = None

    def __init__(self, **kwargs):
        self.parameters = kwargs
        if not self.validate_parameters():
            raise CommandParameterError(
                'Parameter(s) missing, required parameters: {0}'.format(
                    ', '.join(self.required_parameters)))

    def execute(self, output=None, fail_silently=None):
        command = self.get_command()
        output = output if output is not None else self.output
        fail_silently = fail_silently if fail_silently is not None else self.fail_silently

        try:
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            self.pid = process.pid

            std, err = process.communicate()
        except OSError as ex:
            raise CommandExecutionError(ex, 1, self)

        if not fail_silently and (err or process.returncode != 0):
            message = u'Code: {0} Output: {1}'.format(
                process.returncode, u' '.join(err.split('\n')))
            raise CommandExecutionError(message, process.returncode, self)

        return self.handle_output(std) if output else True

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
