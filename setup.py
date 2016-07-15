from __future__ import unicode_literals
import codecs
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as test_command


version = '1.0.1'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


tests_require = [
    'mock==1.3.0',
    'openpyxl==2.2.6',
    'psutil==3.2.1',
    'pytest==2.8.0',
    'pytest-cov==2.1.0',
    'pytest-pep8==1.0.6',
    'pytest-flakes==1.0.1',
    'pytest-django==2.8.0',
    'factory-boy==2.5.2',
    'Pillow==2.9.0',
    'django-anylink==0.3.0',
    'django-treebeard>=4.0',
    'django-cms==3.2.5',
    'django-polymorphic==0.8.1',
    'django-compressor==1.6',
    'django-filer==1.1.1',
]


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


class PyTest(test_command):

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='barbeque',
    description='Helper and tools collection',
    long_description=read('README.rst') + u'\n\n' + read('CHANGELOG.rst'),
    version=version,
    license='BSD',
    author='Moccu GmbH & Co. KG',
    author_email='info@moccu.com',
    url='http://github.com/moccu/barbeque/',
    packages=find_packages(exclude=['barbeque.tests']),
    test_suite='.',
    tests_require=tests_require,
    install_requires=['Django>=1.8,<1.10'],
    extras_require={
        'tests': tests_require,
        'docs': ['sphinx', 'sphinx_rtd_theme'],
        'exporter': ['openpyxl'],
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Django',
    ],
)
