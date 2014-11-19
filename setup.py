#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


class PyTest(TestCommand):
    user_options = [
        ('cov=', None, 'Run coverage'),
        ('cov-xml=', None, 'Generate junit xml report'),
        ('cov-html=', None, 'Generate junit html report'),
        ('junitxml=', None, 'Generate xml of test results'),
        ('clearcache', None, 'Clear cache first')
    ]
    boolean_options = ['clearcache']

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.cov = None
        self.cov_xml = False
        self.cov_html = False
        self.junitxml = None
        self.clearcache = False

    def run_tests(self):
        import pytest

        params = {'args': self.test_args}

        if self.cov is not None:
            params['plugins'] = ['cov']
            params['args'].extend(
                ['--cov', self.cov, '--cov-report', 'term-missing'])
            if self.cov_xml:
                params['args'].extend(['--cov-report', 'xml'])
            if self.cov_html:
                params['args'].extend(['--cov-report', 'html'])
        if self.junitxml is not None:
            params['args'].extend(['--junitxml', self.junitxml])
        if self.clearcache:
            params['args'].extend(['--clearcache'])

        self.test_suite = True

        errno = pytest.main(**params)
        sys.exit(errno)


tests_require = [
    'coverage',
    'mock',
    'openpyxl',
    'psutil',
    'pytest',
    'pytest-cov',
    'pytest-pep8',
    'pytest-flakes',
    'pytest-django',
    'python-coveralls',
    'factory-boy'
]


setup(
    name='barbeque',
    description='Helper and tools collection',
    long_description=read('README.rst') + u'\n\n' + read('CHANGELOG.rst'),
    version='0.1',
    license='BSD',
    author='Stephan Jaekel, Christopher Grebs',
    author_email='info@moccu.com',
    url='http://github.com/moccu/barbeque/',
    packages=find_packages(exclude=['barbeque.tests']),
    test_suite='.',
    tests_require=tests_require,
    install_requires=['six'],
    cmdclass={'test': PyTest},
    extras_require={
        'tests': tests_require,
        'docs': ['sphinx'],
        'tox': ['tox'],
        'dev': ['Django'],
        'exporter': ['openpyxl'],
        'commands': ['psutil'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ],
)
