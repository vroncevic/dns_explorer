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

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDNSResolver(Protocol):
    '''
        Abstract interface for DNS resolution.

        It defines:

            :methods:
                | resolve - Resolves a domain to an IP address.
                | reverse_resolve - Performs reverse DNS lookup for an IP address.
                | resolve_record - Queries specific DNS records for a domain.
                | is_initialized - Checks if the resolver is initialized.
                | __str__ - Returns the DNSResolver as string representation.
    '''

    def resolve(self, domain: str) -> str | None:
        '''
            Resolves a domain name to an IP address.

            :param domain: The domain name to resolve.
            :return: The resolved IP address or None if resolution fails.
        '''

    def reverse_resolve(self, ip: str) -> list[str] | None:
        '''
            Performs reverse DNS lookup on an IP address.

            :param ip: The IP address.
            :return: The list of resolved hostnames or None if lookup fails.
        '''

    def resolve_record(self, domain: str, record_type: str) -> list[str]:
        '''
            Queries specific DNS records for a domain.

            :param domain: The domain name.
            :param record_type: The DNS record type (A, MX, etc.).
            :return: List of record values.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if the resolver is initialized.

            :return: True if initialized, False otherwise.
        '''

    def __str__(self) -> str:
        '''
            Returns the DNSResolver as string representation.

            :return: The DNSResolver as string representation.
        '''
