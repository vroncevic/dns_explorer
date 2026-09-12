# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines abstract interface for services.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from dns_explorer.core.model.dns_record import DNSRecord
from dns_explorer.core.model.resolved_domain import ResolvedDomain

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IService(Protocol):
    '''
        Defines the abstract interface for services.

        It defines:

            :methods:
                | explore - Explores subdomains of a domain.
                | check_dns - Executes dns request and reverse DNS lookup for a single domain.
                | get_records - Queries various DNS records for a domain.
                | reverse_resolve - Performs reverse DNS lookup on an IP address.
                | is_initialized - Checks if the service is initialized.
    '''

    def explore(self, domain: str, cluster: int) -> list[ResolvedDomain]:
        '''
            Explores subdomains of a domain and resolves their DNS and reverse DNS.

            :param domain: Base domain name to explore.
            :param cluster: Number of subdomains in cluster to scan.
            :return: List of resolved domains.
        '''

    def check_dns(self, domain: str) -> ResolvedDomain | None:
        '''
            Executes dns request and reverse DNS lookup for a single domain.

            :param domain: Domain name to check.
            :return: ResolvedDomain instance or None.
        '''

    def get_records(self, domain: str) -> list[DNSRecord]:
        '''
            Queries various DNS records for a domain.

            :param domain: Domain name.
            :return: List of DNS records.
        '''

    def reverse_resolve(self, ip: str) -> list[str]:
        '''
            Performs reverse DNS lookup on an IP address.

            :param ip: IP address to query.
            :return: List of hostnames.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if the service is initialized.

            :return: True if the service is initialized, False otherwise.
        '''
