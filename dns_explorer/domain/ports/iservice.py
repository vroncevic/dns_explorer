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
    Defines abstract interface for tool services.
'''

from abc import ABC, abstractmethod
from dns_explorer.domain.models import ResolvedDomain, DNSRecord

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class IService(ABC):
    '''
        Abstract interface for tool service.

        It defines:

            :attributes: None.
            :methods:
                | explore - Explores DNS subdomains.
                | check_dns - Executes dns request and reverse DNS lookup for a single domain.
                | get_records - Queries various DNS records for a domain.
                | reverse_resolve - Performs reverse DNS lookup on an IP address.
                | is_initialized - Checks if the service is initialized.
    '''

    @abstractmethod
    def explore(self, domain: str, cluster: int, verbose: bool = False) -> list[ResolvedDomain]:
        '''
            Explores subdomains of a domain and resolves their DNS and reverse DNS.

            :param domain: Base domain name to explore.
            :type domain: <str>
            :param cluster: Number of subdomains in cluster to scan.
            :type cluster: <int>
            :param verbose: Enable/Disable verbose logging.
            :type verbose: <bool>
            :return: List of resolved domains.
            :rtype: <list[ResolvedDomain]>
            :exceptions: None.
        '''
        pass

    @abstractmethod
    def check_dns(self, domain: str, verbose: bool = False) -> ResolvedDomain | None:
        '''
            Executes dns request and reverse DNS lookup for a single domain.

            :param domain: Domain name to check.
            :type domain: <str>
            :param verbose: Enable/Disable verbose option.
            :type verbose: <bool>
            :return: ResolvedDomain instance or None.
            :rtype: <ResolvedDomain | None>
            :exceptions: None.
        '''
        pass

    @abstractmethod
    def get_records(self, domain: str) -> list[DNSRecord]:
        '''
            Queries various DNS records for a domain.

            :param domain: Domain name.
            :type domain: <str>
            :return: List of DNS records.
            :rtype: <list[DNSRecord]>
            :exceptions: None.
        '''
        pass

    @abstractmethod
    def reverse_resolve(self, ip: str) -> list[str]:
        '''
            Performs reverse DNS lookup on an IP address.

            :param ip: IP address to query.
            :type ip: <str>
            :return: List of hostnames.
            :rtype: <list[str]>
            :exceptions: None.
        '''
        pass

    @abstractmethod
    def is_initialized(self) -> bool:
        '''
            Checks if the service is initialized.

            :return: True if the service is initialized, False otherwise.
            :rtype: <bool>
            :exceptions: None.
        '''
        pass
