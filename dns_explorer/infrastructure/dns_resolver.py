# -*- coding: UTF-8 -*-

'''
Module
    dns_resolver.py
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
    Defines DNSResolver class implementing DNS resolution adapter.
'''

from __future__ import annotations

from re import search
from socket import gethostbyaddr, herror

from ats_utilities.utils.reflection import to_str
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_empty
from dns.exception import Timeout
from dns.resolver import NXDOMAIN, NoAnswer, resolve

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DNSResolver:
    '''
        Concrete implementation of DNS resolver adapter.

        It defines:

            :attributes: None.
            :methods:
                | resolve - Resolves a domain name to an IP address.
                | reverse_resolve - Performs reverse DNS lookup on an IP address.
                | resolve_record - Queries specific DNS records for a domain.
                | is_initialized - Checks if the resolver is initialized.
                | __str__ - Returns the DNSResolver as string representation.
    '''

    def resolve(self, domain: str) -> str | None:
        '''
            Resolves a domain name to an IP address.

            :param domain: The domain name to resolve.
            :return: The resolved IP address or None.
            :exceptions:
                | ATSTypeError: Domain parameter must be a string.
                | ATSValueError: Domain parameter cannot be empty.
        '''
        ctx: str = 'dns_resolver::resolve(...)'
        istype(domain, str, ctx, 'domain must be a string')
        not_empty(domain, ctx, 'missing domain name')

        try:
            result = resolve(domain)

            if result:
                pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
                match = search(pattern, str(result.rrset))

                if match:
                    return match.group(0)

        except (NXDOMAIN, Timeout, NoAnswer):
            pass

        return None

    def reverse_resolve(self, ip: str) -> list[str] | None:
        '''
            Performs reverse DNS lookup on an IP address.

            :param ip: The IP address.
            :return: The list of resolved hostnames or None.
            :exceptions:
                | ATSTypeError: IP parameter must be a string.
                | ATSValueError: IP parameter cannot be empty.
        '''
        ctx: str = 'dns_resolver::reverse_resolve(...)'
        istype(ip, str, ctx, 'ip must be a string')
        not_empty(ip, ctx, 'missing ip address')

        try:
            result = gethostbyaddr(ip)
            return [result[0]] + result[1]

        except herror:
            return None

    def resolve_record(self, domain: str, record_type: str) -> list[str]:
        '''
            Queries specific DNS records for a domain.

            :param domain: The domain name.
            :param record_type: The DNS record type.
            :return: List of record values.
            :exceptions:
                | ATSTypeError: Domain parameter must be a string.
                | ATSValueError: Domain parameter cannot be empty.
                | ATSTypeError: Record type parameter must be a string.
                | ATSValueError: Record type parameter cannot be empty.
        '''
        ctx: str = 'dns_resolver::resolve_record(...)'
        istype(domain, str, ctx, 'domain must be a string')
        not_empty(domain, ctx, 'missing domain name')
        istype(record_type, str, ctx, 'record_type must be a string')
        not_empty(record_type, ctx, 'missing record type')

        try:
            result = resolve(domain, record_type)
            return [str(rdata) for rdata in result]

        except (NXDOMAIN, Timeout, NoAnswer):
            pass
        except Exception:
            pass

        return []

    def is_initialized(self) -> bool:
        '''
            Checks if the resolver is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return True

    def __str__(self) -> str:
        '''
            Returns the DNSResolver as string representation.

            :return: The DNSResolver as string representation.
            :exceptions: None.
        '''
        return to_str(self)
