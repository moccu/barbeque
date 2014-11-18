#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbeque.tests.settings')

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'barbeque'
copyright = '2014, Moccu GmbH & Co. KG'
version = '0.1'
release = '0.1'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
# html_static_path = ['_static']
htmlhelp_basename = 'barbequedoc'
latex_documents = [(
    'index', 'barbeque.tex', 'barbeque Documentation',
    'Moccu GmbH & Co. KG', 'manual'
)]
man_pages = [(
    'index', 'barbeque', 'barbeque Documentation',
    ['Moccu GmbH & Co. KG'], 1
)]
texinfo_documents = [(
    'index', 'barbeque', 'barbeque Documentation',
    'Moccu GmbH & Co. KG', 'barbeque', 'Helper and tools collection.',
    'Miscellaneous'
)]
intersphinx_mapping = {'http://docs.python.org/': None}
