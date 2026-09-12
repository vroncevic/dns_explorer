# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Encapsulates core dns_explorer components for simplification of dns_explorer bundle.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle

from dns_explorer.core.service.iservice import IService
from dns_explorer.core.service.idns_resolver import IDNSResolver
from dns_explorer.infrastructure.cli.icli import ICLI
from dns_explorer.setup.bundle import DNSExplorerBundle
from dns_explorer.setup.validator import DNSExplorerBundleValidator
from dns_explorer.setup.keys import DNSExplorerBundleKeys
from dns_explorer.setup.dependencies import DNSExplorerBundleDependencies
from dns_explorer.setup.dep_validator import DNSExplorerBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DNSExplorerBundleRegistry:
    '''
        Encapsulates core dns_explorer components for simplification of dns_explorer bundle.

        It defines:

            :methods:
                | create_bundle - Creates the dns_explorer bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: DNSExplorerBundleDependencies) -> DNSExplorerBundle:
        '''
            Creates the dns_explorer bundle.

            :param dependencies: The dns_explorer bundle dependencies.
            :return: The dns_explorer bundle.
            :exceptions:
                | ATSValueError: The dns_explorer bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The dns_explorer bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The dns_explorer bundle must be provided and have proper values.
                | ATSTypeError:  The dns_explorer bundle must be an instance of DNSExplorerBundle and
                |                its attributes must be instances of their respective types.
        '''
        DNSExplorerBundleDependenciesValidator.validate(dependencies)

        base: BaseBundle | None = dependencies.get(DNSExplorerBundleKeys.DEPENDENCY_BASE) if dependencies else None
        service: IService | None = dependencies.get(DNSExplorerBundleKeys.DEPENDENCY_SERVICE) if dependencies else None
        dns_resolver: IDNSResolver | None = dependencies.get(DNSExplorerBundleKeys.DEPENDENCY_DNS_RESOLVER) if dependencies else None
        cli: ICLI | None = dependencies.get(DNSExplorerBundleKeys.DEPENDENCY_CLI) if dependencies else None

        bundle: DNSExplorerBundle = DNSExplorerBundle(
            base=base, service=service, dns_resolver=dns_resolver, cli=cli
        )

        DNSExplorerBundleValidator.validate(bundle)

        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version.
            :exceptions: None.
        '''
        return __version__
