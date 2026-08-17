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
    Runtime components and interface constraints for the dns_explorer bundle.
'''

from __future__ import annotations

from typing import ClassVar
from types import MappingProxyType

from ats_utilities.base.setup.bundle import BaseBundle

from dns_explorer.core.service.iservice import IService
from dns_explorer.core.service.idns_resolver import IDNSResolver
from dns_explorer.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DNSExplorerBundleKeys:
    '''
        Runtime components and interface constraints for the dns_explorer bundle.

        It defines:

            :attributes:
                | DEPENDENCY_BASE - The base bundle constant for the dns_explorer bundle.
                | DEPENDENCY_SERVICE - The service interface constant for the dns_explorer bundle.
                | DEPENDENCY_DNS_RESOLVER - The dns_resolver interface constant for the dns_explorer bundle.
                | DEPENDENCY_CLI - The cli interface constant for the dns_explorer bundle.
                | OPTION_INFO_FILE - The info file option constant for the dns_explorer bundle.
            :methods:
                | get_dependency_to_type - Returns the mapping of the dns_explorer bundle dependencies to their types.
                | get_option_to_type - Returns the mapping of the dns_explorer bundle options to their types.
    '''

    # Dependency Keys
    DEPENDENCY_BASE: ClassVar[str] = 'base'
    DEPENDENCY_SERVICE: ClassVar[str] = 'service'
    DEPENDENCY_DNS_RESOLVER: ClassVar[str] = 'dns_resolver'
    DEPENDENCY_CLI: ClassVar[str] = 'cli'

    # Option Keys
    OPTION_INFO_FILE: ClassVar[str] = 'info_file'

    @classmethod
    def get_dependency_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of the dns_explorer bundle dependencies to their types.

            :return: The mapping of the dns_explorer bundle dependencies to their types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.DEPENDENCY_BASE: BaseBundle,
            cls.DEPENDENCY_SERVICE: IService,
            cls.DEPENDENCY_DNS_RESOLVER: IDNSResolver,
            cls.DEPENDENCY_CLI: ICLI,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of the dns_explorer bundle options to their types.

            :return: The mapping of the dns_explorer bundle options to their types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_INFO_FILE: str,
        })
