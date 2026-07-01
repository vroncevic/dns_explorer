# -*- coding: UTF-8 -*-

'''
Module
    test_service.py
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
    Unit tests for application service.
'''

import unittest
from unittest.mock import MagicMock
from dns_explorer.domain.ports.idns_resolver import IDNSResolver
from dns_explorer.application.service import Service
from dns_explorer.domain.models import ResolvedDomain, DNSRecord

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class MockDNSResolver(IDNSResolver):
    '''
        Mock DNS resolver for testing.
    '''
    def __init__(self, resolve_fails: bool = False, reverse_fails: bool = False) -> None:
        self.resolve_fails = resolve_fails
        self.reverse_fails = reverse_fails
        self.resolved_domains: list[str] = []
        self.reversed_ips: list[str] = []

    def resolve(self, domain: str) -> str | None:
        self.resolved_domains.append(domain)
        if self.resolve_fails:
            return None
        return "1.2.3.4"

    def reverse_resolve(self, ip: str) -> list[str] | None:
        self.reversed_ips.append(ip)
        if self.reverse_fails:
            return None
        return ["host.domain.com"]

    def resolve_record(self, domain: str, record_type: str) -> list[str]:
        if self.resolve_fails:
            return []
        if record_type == "A":
            return ["1.2.3.4"]
        elif record_type == "MX":
            return ["10 mail.google.com"]
        return [f"value_{record_type}"]

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return "MockDNSResolver"


class TestService(unittest.TestCase):
    '''
        Defines application service unit tests.

        It defines:

            :attributes: None
            :methods:
                | test_init_success - Tests successful service initialization.
                | test_init_missing_dns_resolver - Tests initialization fails when dns_resolver is None.
                | test_execute_missing_args - Tests execution fails when arguments are missing.
                | test_execute_explore_success - Tests service execute for explore command.
                | test_check_dns_success - Tests successful single domain check.
                | test_check_dns_fails - Tests single domain check failure conditions.
                | test_get_records_success - Tests retrieving multiple record types.
                | test_get_records_fails - Tests failures in retrieving records.
    '''

    def test_init_success(self) -> None:
        '''
            Tests successful service initialization.

            :raises None.
        '''
        mock_resolver: MockDNSResolver = MockDNSResolver()
        service: Service = Service(dns_resolver=mock_resolver)
        self.assertIsNotNone(service)
        self.assertTrue(service.is_initialized())
        self.assertTrue(isinstance(str(service), str))
        self.assertNotEqual(str(service), "")

    def test_init_missing_dns_resolver(self) -> None:
        '''
            Tests initialization fails when dns_resolver is None.

            :raises ValueError: When dns_resolver is None.
        '''
        with self.assertRaises(ValueError):
            Service(dns_resolver=None)

    def test_execute_missing_args(self) -> None:
        '''
            Tests execution fails when params is None or empty.

            :raises ValueError: When params is None.
        '''
        mock_resolver: MockDNSResolver = MockDNSResolver()
        service: Service = Service(dns_resolver=mock_resolver)

        with self.assertRaises(ValueError):
            service.explore("", 1)

    def test_execute_explore_success(self) -> None:
        '''
            Tests service execute for explore command.
        '''
        mock_resolver: MockDNSResolver = MockDNSResolver()
        service: Service = Service(dns_resolver=mock_resolver)

        res = service.explore("google.com", 2, True)
        self.assertTrue(isinstance(res, list))
        self.assertTrue(isinstance(res[0], ResolvedDomain))
        self.assertEqual(res[0].domain, "www.google.com")
        self.assertEqual(res[0].ip, "1.2.3.4")
        self.assertEqual(res[0].reverse, ["host.domain.com"])

        # www + www0 + www1 (cluster count = 2) for each subdomain.
        # Total subdomains is 30. Each subdomain is checked 3 times.
        # Total resolved domains should be 30 * 3 = 90.
        self.assertEqual(len(mock_resolver.resolved_domains), len(Service._SUBDOMAINS) * 3)

    def test_check_dns_success(self) -> None:
        '''
            Tests successful single domain check.
        '''
        mock_resolver: MockDNSResolver = MockDNSResolver()
        service: Service = Service(dns_resolver=mock_resolver)
        res = service.check_dns("google.com")
        self.assertIsNotNone(res)
        self.assertEqual(res.domain, "google.com")
        self.assertEqual(res.ip, "1.2.3.4")
        self.assertEqual(res.reverse, ["host.domain.com"])

    def test_check_dns_fails(self) -> None:
        '''
            Tests single domain check failure conditions.
        '''
        mock_resolver: MockDNSResolver = MockDNSResolver(resolve_fails=True)
        service: Service = Service(dns_resolver=mock_resolver)

        res = service.check_dns("google.com")
        self.assertIsNone(res)

        mock_resolver_reverse_fail: MockDNSResolver = MockDNSResolver(reverse_fails=True)
        service_reverse_fail: Service = Service(dns_resolver=mock_resolver_reverse_fail)
        res_reverse = service_reverse_fail.check_dns("google.com")
        self.assertIsNone(res_reverse)

        mock_resolver_exception: MockDNSResolver = MockDNSResolver()
        mock_resolver_exception.resolve = MagicMock(side_effect=RuntimeError("Resolution failed"))
        service_exception: Service = Service(dns_resolver=mock_resolver_exception)
        res_exception = service_exception.check_dns("google.com")
        self.assertIsNone(res_exception)

    def test_get_records_success(self) -> None:
        '''
            Tests retrieving multiple record types.
        '''
        mock_resolver: MockDNSResolver = MockDNSResolver()
        service: Service = Service(dns_resolver=mock_resolver)
        res = service.get_records("google.com")
        self.assertTrue(len(res) > 0)
        self.assertTrue(any(r.record_type == "A" and r.value == "1.2.3.4" for r in res))
        self.assertTrue(any(r.record_type == "MX" and r.value == "10 mail.google.com" for r in res))

    def test_get_records_fails(self) -> None:
        '''
            Tests failures in retrieving records.
        '''
        mock_resolver: MockDNSResolver = MockDNSResolver()
        service: Service = Service(dns_resolver=mock_resolver)

        with self.assertRaises(ValueError):
            service.get_records("")

        # Test where resolver resolve_record raises an exception
        mock_resolver_exception = MockDNSResolver()
        mock_resolver_exception.resolve_record = MagicMock(side_effect=RuntimeError("Failure"))
        service_exception = Service(dns_resolver=mock_resolver_exception)
        res = service_exception.get_records("google.com")
        self.assertEqual(res, [])

    def test_reverse_resolve_success(self) -> None:
        '''
            Tests successful reverse resolution.
        '''
        mock_resolver: MockDNSResolver = MockDNSResolver()
        service: Service = Service(dns_resolver=mock_resolver)
        res = service.reverse_resolve("1.2.3.4")
        self.assertEqual(res, ["host.domain.com"])

    def test_reverse_resolve_fails(self) -> None:
        '''
            Tests reverse resolution failure conditions.
        '''
        mock_resolver: MockDNSResolver = MockDNSResolver()
        service: Service = Service(dns_resolver=mock_resolver)

        with self.assertRaises(ValueError):
            service.reverse_resolve("")

        mock_resolver_fail: MockDNSResolver = MockDNSResolver(reverse_fails=True)
        service_fail: Service = Service(dns_resolver=mock_resolver_fail)
        res = service_fail.reverse_resolve("1.2.3.4")
        self.assertEqual(res, [])

        mock_resolver_exception = MockDNSResolver()
        mock_resolver_exception.reverse_resolve = MagicMock(side_effect=RuntimeError("Failure"))
        service_exception = Service(dns_resolver=mock_resolver_exception)
        res_ex = service_exception.reverse_resolve("1.2.3.4")
        self.assertEqual(res_ex, [])

