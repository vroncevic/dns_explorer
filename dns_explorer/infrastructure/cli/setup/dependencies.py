# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    CLI bundle dependencies for the CLI bundle.
'''

from __future__ import annotations

from typing import TypedDict
from collections.abc import Sequence

from ats_utilities.option.imanager import IOptionManager

from dns_explorer.core.service.iservice import IService
from dns_explorer.infrastructure.command.command import CommandBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleDependencies(TypedDict):
    '''
        CLI bundle dependencies for the CLI bundle.

        It defines:

            :attributes:
                | service - The service orchestrating the tools execution.
                | parser - The argument parser for parsing CLI command arguments.
                | commands - The sequence of command bundles.
    '''

    service: IService
    parser: IOptionManager
    commands: Sequence[CommandBundle]
