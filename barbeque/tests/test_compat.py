

from barbeque.compat import StringIO, UnicodeWriter


class TestUnicodeWriter:
    def test_writerow(self):
        output = StringIO()

        with UnicodeWriter(output) as writer:
            writer.writerow(['test'])
            writer.writerow(['test2'])

        assert output.getvalue() == 'test\r\ntest2\r\n'

    def test_writerows(self):
        output = StringIO()

        with UnicodeWriter(output) as writer:
            writer.writerows([['test'], ['test2']])

        assert output.getvalue() == 'test\r\ntest2\r\n'
