# -*- coding: utf-8 -*-

'''
Module
    conf.py
Copyright
    Copyright (C) 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    dns_explorer is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    dns_explorer is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines properties for sphinx-doc.
'''

import os
import sys

from typing import Any, List, Dict, Tuple

sys.path.insert(0, os.path.abspath('../../'))

project: str = 'dns_explorer'
project_copyright: str = '2024, Vladimir Roncevic <elektron.ronca@gmail.com>'
author: str = 'Vladimir Roncevic <elektron.ronca@gmail.com>'
version: str = '1.0.3'
release: str = 'https://github.com/vroncevic/dns_explorer/releases'
extensions: List[str] = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path: List[str] = ['_templates']
source_suffix: str = '.rst'
master_doc: str = 'index'
language: str = 'en'
exclude_patterns: List[str] = []
pygments_style: str = 'sphinx'
html_theme: str = 'classic'
html_static_path: List[str] = ['_static']
htmlhelp_basename: str = 'dns_explorerdoc'
latex_elements: Dict[Any, Any] = {}
latex_documents: List[Tuple[Any, ...]] = [(
    master_doc, 'dns_explorer.tex', 'dns_explorer Documentation',
    'Vladimir Roncevic \\textless{}elektron.ronca@gmail.com\\textgreater{}',
    'manual'
)]
man_pages: List[Tuple[Any, ...]] = [(
    master_doc, 'dns_explorer', 'dns_explorer Documentation', [author], 1
)]
texinfo_documents: List[Tuple[Any, ...]] = [(
    master_doc, 'dns_explorer', 'dns_explorer Documentation', author,
    'dns_explorer', 'One line description of project.', 'Miscellaneous'
)]
epub_title: str = project
epub_exclude_files: List[str] = ['search.html']
