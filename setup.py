from __future__ import unicode_literals
import codecs
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as test_command


version = '1.8.0'


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
    'openpyxl==2.4.8',
    'psutil==5.3.0',
    'pytest==3.2.1',
    'pytest-cov==2.5.1',
    'pytest-pep8==1.0.6',
    'pytest-flakes==2.0.0',
    'pytest-django==3.1.2',
    'pytest-isort==0.1.0',
    'factory-boy>=2.9.2',
    'Pillow==4.2.1',
    'django-anylink==0.4.2',
    'django-treebeard==4.1.2',
    'django-cms==3.4.4',
    'django-polymorphic==1.3',
    'django-compressor==2.2',
    'django-filer==1.2.8',
    'django-floppyforms==1.7.0',
    'easy-thumbnails==2.4.1',
    'mock==2.0.0',
    'tox==2.8.1',
    'tox-pyenv==1.1.0',
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
        'Django>=1.8,<2.0',
        'python-dateutil>=2.4.0',
    ],
    extras_require={
        'tests': tests_require,
        'docs': ['sphinx', 'sphinx_rtd_theme'],
        'exporter': ['openpyxl>=2.4.8,<2.5'],
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
