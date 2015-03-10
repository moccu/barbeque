import sys
import csv

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


PY3 = sys.version > '3'


# Based on http://python3porting.com/problems.html#csv-api-changes
class UnicodeWriter(object):
    def __init__(self, fobj, dialect=csv.excel, encoding='utf-8', **kw):
        self.fobj = fobj
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw

    def __enter__(self):
        self.writer = csv.writer(self.fobj, dialect=self.dialect, **self.kw)
        return self

    def __exit__(self, type, value, traceback):
        pass

    def writerow(self, row):
        if not PY3:
            row = [s.encode(self.encoding) for s in row]
        self.writer.writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
