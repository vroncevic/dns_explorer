# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Defines the dns_explorer bundle.
'''

from __future__ import annotations

from dataclasses import dataclass

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.utils.reflection import instance_to_dict

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


@dataclass(slots=True, frozen=True, kw_only=True)
class DNSExplorerBundle:
    '''
        DNSExplorer bundle holding the components of the dns_explorer.

        It defines:

            :attributes:
                | base - The base bundle with the base components.
                | service - The service orchestrating the dns_explorer's execution.
                | dns_resolver - The adapter performing DNS resolutions.
                | cli - The command-line interface adapter.
            :methods:
                | to_dict - Converts the dns_explorer bundle to a dictionary.
    '''

    base: BaseBundle
    service: IService
    dns_resolver: IDNSResolver
    cli: ICLI

    def to_dict(self) -> dict[str, object]:
        '''
            Converts the dns_explorer bundle to a dictionary.

            :return: Dictionary representation of the dns_explorer bundle.
            :exceptions: None.
        '''
        return instance_to_dict(self)
