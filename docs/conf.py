#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from os.path import abspath, join, dirname
import pkg_resources

sys.path.append(abspath(join(dirname(__file__), "_ext")))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbeque.tests.settings')

try:
    import sphinx_rtd_theme
except ImportError:
    sphinx_rtd_theme = None

distribution = pkg_resources.get_distribution('barbeque')

version = distribution.version
release = version

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'barbequedocs'
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'barbeque'
copyright = r'2015, Moccu GmbH \& Co. KG'
version = version
release = version
exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_domain_indices = True

if sphinx_rtd_theme:
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
else:
    html_theme = 'default'

html_static_path = ['_static']

# html_static_path = ['_static']
htmlhelp_basename = 'barbequedoc'
latex_documents = [(
    'index', 'barbeque.tex', 'barbeque Documentation',
    r'Moccu GmbH \& Co. KG', 'manual'
)]
man_pages = [(
    'index', 'barbeque', 'barbeque Documentation',
    [r'Moccu GmbH \& Co. KG'], 1
)]
texinfo_documents = [(
    'index', 'barbeque', 'barbeque Documentation',
    r'Moccu GmbH \& Co. KG', 'barbeque', 'Helper and tools collection.',
    'Miscellaneous'
)]

intersphinx_mapping = {
    'python': ('http://docs.python.org/', None),
    'filer': ('http://django-filer.readthedocs.org/en/latest/', None),
    'django': (
        'http://docs.djangoproject.com/en/dev/',
        'http://docs.djangoproject.com/en/dev/_objects/'
    ),
}
