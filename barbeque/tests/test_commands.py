import pytest
from django.utils.datastructures import SortedDict

from barbeque.compat import PY3
from barbeque.commands.base import CommandParameterError, CommandExecutionError, Command
from barbeque.commands.imaging import GmConvertCommand, SvgoCommand


class OutputCommand(Command):
    command = 'echo "{words}"'
    required_parameters = ['words']


class InvalidCommand(Command):
    command = 'thiscommanddoesnotexist'


class RetValCommand(Command):
    command = 'sh -c "exit {code}"'
    required_parameters = ['code']


class StderrCommand(Command):
    command = 'sh -c "echo \'{words}\' >&2"'
    required_parameters = ['words']


class TestCommand:
    def test_missing_parameters(self):
        with pytest.raises(CommandParameterError) as exc:
            RetValCommand()

        assert 'code' in str(exc.value)

    def test_execute(self):
        cmd = OutputCommand(words='test')
        assert cmd.execute() is True

    def test_execute_output(self):
        cmd = OutputCommand(words='test')
        assert cmd.execute(ignore_output=False) == 'test\n'

    @pytest.mark.skipif(PY3, reason='Needs Python2')
    def test_failing_oserror_py2(self):
        with pytest.raises(CommandExecutionError) as exc:
            cmd = InvalidCommand()
            cmd.execute()

        assert exc.value.code == 1
        assert exc.value.command == cmd
        assert exc.value.stderr == "[Errno 2] No such file or directory"

    @pytest.mark.skipif(not PY3, reason='Needs Python3')
    def test_failing_oserror_py3(self):
        with pytest.raises(CommandExecutionError) as exc:
            cmd = InvalidCommand()
            cmd.execute()

        assert exc.value.code == 1
        assert exc.value.command == cmd
        assert exc.value.stderr == (
            "[Errno 2] No such file or directory: 'thiscommanddoesnotexist'")

    def test_failing_return_value(self):
        with pytest.raises(CommandExecutionError) as exc:
            cmd = RetValCommand(code=23)
            cmd.execute()

        assert exc.value.code == 23
        assert exc.value.command == cmd
        assert exc.value.stderr == ''

    def test_failing_return_value_silent(self):
        cmd = RetValCommand(code=23)
        assert cmd.execute(fail_silently=True) is True

    def test_failing_stderr(self):
        with pytest.raises(CommandExecutionError) as exc:
            cmd = StderrCommand(words='test 123')
            cmd.execute()

        assert exc.value.code == 0
        assert exc.value.command == cmd
        assert exc.value.stderr == 'test 123\n'

    def test_failing_stderr_silent(self):
        cmd = StderrCommand(words='test 123')
        assert cmd.execute(fail_silently=True) is True


class TestGmConvertCommand:
    def test_get_command(self):
        options = SortedDict()
        options['trueflag'] = True
        options['+falseflag'] = True
        options['valueflag'] = 'somevalue'

        cmd = GmConvertCommand(infile='in.jpg', outfile='out.jpg', options=options)

        assert cmd.get_command() == [
            'gm',
            'convert',
            'in.jpg',
            '-trueflag',
            '+falseflag',
            '-valueflag', 'somevalue',
            'out.jpg'
        ]


class TestSvgoCommand:
    def test_get_command(self):
        cmd = SvgoCommand(infile='in.jpg', outfile='out.jpg')

        assert cmd.get_command() == [
            'svgo',
            '-i', 'in.jpg',
            '-o', 'out.jpg'
        ]
