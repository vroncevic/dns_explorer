# -*- coding: UTF-8 -*-

'''
Module
    test_models.py
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
    Unit tests for domain models.
'''

import unittest
from dns_explorer.domain.models import ResolvedDomain, DNSRecord

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class TestModels(unittest.TestCase):
    '''
        Defines domain models unit tests.
    '''

    def test_resolved_domain_model(self) -> None:
        '''
            Tests ResolvedDomain instantiation and attributes.
        '''
        model = ResolvedDomain(
            domain="google.com",
            ip="1.2.3.4",
            reverse=["host.google.com"]
        )
        self.assertEqual(model.domain, "google.com")
        self.assertEqual(model.ip, "1.2.3.4")
        self.assertEqual(model.reverse, ["host.google.com"])

    def test_dns_record_model(self) -> None:
        '''
            Tests DNSRecord instantiation and attributes.
        '''
        model = DNSRecord(record_type="A", value="1.2.3.4")
        self.assertEqual(model.record_type, "A")
        self.assertEqual(model.value, "1.2.3.4")
