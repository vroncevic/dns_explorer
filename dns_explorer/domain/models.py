# -*- coding: UTF-8 -*-

'''
Module
    models.py
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
    Defines domain models representing tool parameters and results.
'''

from dataclasses import dataclass

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


@dataclass
class ResolvedDomain:
    '''
        Domain model representing a resolved domain, its IP, and reverse hostnames.

        It defines:

            :attributes:
                | domain - Resolved domain name.
                | ip - IP address of the domain.
                | reverse - List of reverse DNS hostnames.
    '''

    domain: str
    ip: str
    reverse: list[str]


@dataclass
class DNSRecord:
    '''
        Domain model representing a DNS record.

        It defines:

            :attributes:
                | record_type - Type of the DNS record (A, MX, TXT, etc.).
                | value - String representation of the record value.
    '''

    record_type: str
    value: str
