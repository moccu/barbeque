from __future__ import unicode_literals
import codecs
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as test_command


version = '1.5.1'


# TEMPORARY FIX FOR
# https://bitbucket.org/pypa/setuptools/issues/450/egg_info-command-is-very-slow-if-there-are
TO_OMIT = ['.git', '.tox']
orig_os_walk = os.walk


def patched_os_walk(path, *args, **kwargs):
    for (dirpath, dirnames, filenames) in orig_os_walk(path, *args, **kwargs):
        if '.git' in dirnames:
            # We're probably in our own root directory.
            print("MONKEY PATCH: omitting a few directories like .git and .tox...")
            dirnames[:] = list(set(dirnames) - set(TO_OMIT))
        yield (dirpath, dirnames, filenames)

os.walk = patched_os_walk
# END IF TEMPORARY FIX.


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
    'pytest==3.0.3',
    'pytest-cov==2.3.1',
    'pytest-pep8==1.0.6',
    'pytest-flakes==1.0.1',
    'pytest-django==3.0.0',
    'pytest-isort==0.1.0',
    'factory-boy>=2.8.1,<2.9',
    'Pillow==3.4.0',
    'django-anylink==0.3.0',
    'django-treebeard>=4.0',
    'django-cms==3.3.3',
    'django-polymorphic==0.8.1',
    'django-compressor==1.6',
    'django-filer==1.1.1',
    'django-floppyforms==1.7.0',
    'tox==2.3.1',
    'tox-pyenv==1.0.3',
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
    packages=find_packages(exclude=['barbeque.tests', 'barbeque.tests.*']),
    include_package_data=True,
    test_suite='.',
    tests_require=tests_require,
    install_requires=[
        'Django>=1.8,<1.10',
        'python-dateutil>=2.4.0',
    ],
    extras_require={
        'tests': tests_require,
        'docs': ['sphinx', 'sphinx_rtd_theme'],
        'exporter': ['openpyxl>=2.4.1,<2.5'],
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
