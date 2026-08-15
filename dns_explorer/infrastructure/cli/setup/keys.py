# -*- coding: UTF-8 -*-

'''
Module
    keys.py
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
    Runtime components and interface constraints for the CLI bundle.
'''

from __future__ import annotations

from typing import ClassVar
from types import MappingProxyType
from collections.abc import Sequence

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


class CLIBundleKeys:
    '''
        Runtime components and interface constraints for the CLI bundle.

        It defines:

            :attributes:
                | DEPENDENCY_SERVICE - The service interface constant.
                | DEPENDENCY_PARSER - The parser interface constant.
                | DEPENDENCY_COMMANDS - The commands sequence constant.
                | OPTION_SERVICE - The service option constant.
                | OPTION_PARSER - The parser option constant.
                | OPTION_CONTEXT_BUNDLE - The context bundle option constant.
            :methods:
                | get_dependency_to_type - Returns the mapping of CLI dependencies to their types.
                | get_option_to_type - Returns the mapping of CLI options to their types.
    '''

    # Dependency Keys
    DEPENDENCY_SERVICE: ClassVar[str] = 'service'
    DEPENDENCY_PARSER: ClassVar[str] = 'parser'
    DEPENDENCY_COMMANDS: ClassVar[str] = 'commands'

    # Option Keys
    OPTION_SERVICE: ClassVar[str] = 'service'
    OPTION_PARSER: ClassVar[str] = 'parser'
    OPTION_CONTEXT_BUNDLE: ClassVar[str] = 'context_bundle'

    @classmethod
    def get_dependency_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of CLI dependencies to their types.

            :return: The mapping of CLI dependencies to their types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.DEPENDENCY_SERVICE: IService,
            cls.DEPENDENCY_PARSER: IOptionManager,
            cls.DEPENDENCY_COMMANDS: Sequence,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of CLI options to their types.

            :return: The mapping of CLI options to their types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_SERVICE: IService,
            cls.OPTION_PARSER: IOptionManager,
            cls.OPTION_CONTEXT_BUNDLE: ContextBundle,
        })
