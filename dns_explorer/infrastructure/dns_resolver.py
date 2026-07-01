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
    Defines DNSResolver class implementing IDNSResolver.
'''

import re
import socket
from typing import override
from dns.resolver import resolve, NXDOMAIN, NoAnswer
from dns.exception import Timeout
from ats_utilities.exceptions.ats_type_error import ATSTypeError
from ats_utilities.exceptions.ats_value_error import ATSValueError
from ats_utilities.factory_class import format_instance_to_string
from dns_explorer.domain.ports.idns_resolver import IDNSResolver

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class DNSResolver(IDNSResolver):
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

    @override
    def resolve(self, domain: str) -> str | None:
        '''
            Resolves a domain name to an IP address.

            :param domain: The domain name to resolve.
            :type domain: <str>
            :return: The resolved IP address or None.
            :rtype: <str | None>
            :exceptions:
                | ATSTypeError: Domain parameter must be a string.
                | ATSValueError: Domain parameter cannot be empty.
        '''
        if not isinstance(domain, str):
            raise ATSTypeError("domain must be a string")
        if not domain:
            raise ATSValueError("missing domain name")

        try:
            result = resolve(domain)
            if result:
                pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
                match = re.search(pattern, str(result.rrset))
                if match:
                    return match.group(0)
        except (NXDOMAIN, Timeout, NoAnswer):
            pass
        return None

    @override
    def reverse_resolve(self, ip: str) -> list[str] | None:
        '''
            Performs reverse DNS lookup on an IP address.

            :param ip: The IP address.
            :type ip: <str>
            :return: The list of resolved hostnames or None.
            :rtype: <list[str] | None>
            :exceptions:
                | ATSTypeError: IP parameter must be a string.
                | ATSValueError: IP parameter cannot be empty.
        '''
        if not isinstance(ip, str):
            raise ATSTypeError("ip must be a string")
        if not ip:
            raise ATSValueError("missing ip address")

        try:
            result = socket.gethostbyaddr(ip)
            return [result[0]] + result[1]
        except socket.herror:
            return None

    @override
    def resolve_record(self, domain: str, record_type: str) -> list[str]:
        '''
            Queries specific DNS records for a domain.

            :param domain: The domain name.
            :type domain: <str>
            :param record_type: The DNS record type.
            :type record_type: <str>
            :return: List of record values.
            :rtype: <list[str]>
            :exceptions:
                | ATSTypeError: Domain parameter must be a string.
                | ATSValueError: Domain parameter cannot be empty.
                | ATSTypeError: Record type parameter must be a string.
                | ATSValueError: Record type parameter cannot be empty.
        '''
        if not isinstance(domain, str):
            raise ATSTypeError("domain must be a string")

        if not domain:
            raise ATSValueError("missing domain name")

        if not isinstance(record_type, str):
            raise ATSTypeError("record_type must be a string")

        if not record_type:
            raise ATSValueError("missing record type")

        try:
            result = resolve(domain, record_type)
            return [str(rdata) for rdata in result]
        except (NXDOMAIN, Timeout, NoAnswer):
            pass
        except Exception:
            pass
        return []

    @override
    def is_initialized(self) -> bool:
        '''
            Checks if the resolver is initialized.

            :return: True if initialized, False otherwise.
            :rtype: <bool>
            :exceptions: None.
        '''
        return True

    @override
    def __str__(self) -> str:
        '''
            Returns the DNSResolver as string representation.

            :return: The DNSResolver as string representation.
            :rtype: <str>
            :exceptions: None.
        '''
        return format_instance_to_string(self)
