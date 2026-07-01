# -*- coding: UTF-8 -*-

'''
Module
    idns_resolver.py
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
    Defines abstract interface for DNS resolution operations.
'''

from abc import ABC, abstractmethod

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class IDNSResolver(ABC):
    '''
        Abstract interface for DNS resolution.

        It defines:

            :attributes: None.
            :methods:
                | resolve - Resolves a domain to an IP address.
                | reverse_resolve - Performs reverse DNS lookup for an IP address.
                | resolve_record - Queries specific DNS records for a domain.
                | is_initialized - Checks if the resolver is initialized.
                | __str__ - Returns the DNSResolver as string representation.
    '''

    @abstractmethod
    def resolve(self, domain: str) -> str | None:
        '''
            Resolves a domain name to an IP address.

            :param domain: The domain name to resolve.
            :type domain: <str>
            :return: The resolved IP address or None if resolution fails.
            :rtype: <str | None>
            :exceptions: None.
        '''
        pass

    @abstractmethod
    def reverse_resolve(self, ip: str) -> list[str] | None:
        '''
            Performs reverse DNS lookup on an IP address.

            :param ip: The IP address.
            :type ip: <str>
            :return: The list of resolved hostnames or None if lookup fails.
            :rtype: <list[str] | None>
            :exceptions: None.
        '''
        pass

    @abstractmethod
    def resolve_record(self, domain: str, record_type: str) -> list[str]:
        '''
            Queries specific DNS records for a domain.

            :param domain: The domain name.
            :type domain: <str>
            :param record_type: The DNS record type (A, MX, etc.).
            :type record_type: <str>
            :return: List of record values.
            :rtype: <list[str]>
            :exceptions: None.
        '''
        pass

    @abstractmethod
    def is_initialized(self) -> bool:
        '''
            Checks if the resolver is initialized.

            :return: True if initialized, False otherwise.
            :rtype: <bool>
            :exceptions: None.
        '''
        pass

    @abstractmethod
    def __str__(self) -> str:
        '''
            Returns the DNSResolver as string representation.

            :return: The DNSResolver as string representation.
            :rtype: <str>
            :exceptions: None.
        '''
        pass
