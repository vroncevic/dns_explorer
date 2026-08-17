# -*- coding: UTF-8 -*-

'''
Module
    options.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
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
    Encapsulates core CLI components for simplification of CLI bundle options.
'''

from __future__ import annotations

from typing import TypedDict

from ats_utilities.option.imanager import IOptionManager
from ats_utilities.context.bundle import ContextBundle

from dns_explorer.core.service.iservice import IService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleOptions(TypedDict):
    '''
        Encapsulates core CLI components for simplification of CLI bundle options.

        It defines:

            :attributes:
                | service - The service for core execution.
                | parser - The parser for command line options.
                | context_bundle - The context bundle for command execution.
    '''

    service: IService
    parser: IOptionManager
    context_bundle: ContextBundle
