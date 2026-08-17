# -*- coding: UTF-8 -*-

'''
Module
    dns_resolver_test.py
Info
    Unit tests for DNSResolver class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from dns_explorer.infrastructure.dns_resolver import DNSResolver


class TestDNSResolver(unittest.TestCase):
    def test_init_success(self) -> None:
        resolver = DNSResolver()
        self.assertTrue(resolver.is_initialized())

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_success(self, mock_resolve: Mock) -> None:
        mock_answer = Mock()
        mock_answer.rrset = Mock()
        mock_answer.rrset.__str__ = Mock(return_value="google.com. 300 IN A 142.251.143.238")
        mock_resolve.return_value = mock_answer

        resolver = DNSResolver()
        result = resolver.resolve("google.com")
        self.assertEqual(result, "142.251.143.238")

    @patch('socket.gethostbyaddr')
    def test_reverse_resolve_success(self, mock_gethostbyaddr: Mock) -> None:
        mock_gethostbyaddr.return_value = ("dns.google", [], ["8.8.8.8"])

        resolver = DNSResolver()
        result = resolver.reverse_resolve("8.8.8.8")
        self.assertEqual(result, ["dns.google"])

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_record_success(self, mock_resolve: Mock) -> None:
        mock_answer = Mock()
        mock_answer.__iter__ = Mock(return_value=iter(["142.251.143.238"]))
        mock_resolve.return_value = mock_answer

        resolver = DNSResolver()
        result = resolver.resolve_record("google.com", "A")
        self.assertEqual(result, ["142.251.143.238"])

    def test_str_representation(self) -> None:
        resolver = DNSResolver()
        self.assertTrue(isinstance(str(resolver), str))

    def test_resolve_invalid_type(self) -> None:
        resolver = DNSResolver()
        from ats_utilities.exceptions.ats_type_error import ATSTypeError
        with self.assertRaises(ATSTypeError):
            resolver.resolve(123)

    def test_resolve_empty(self) -> None:
        resolver = DNSResolver()
        from ats_utilities.exceptions.ats_value_error import ATSValueError
        with self.assertRaises(ATSValueError):
            resolver.resolve("")

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_falsy(self, mock_resolve: Mock) -> None:
        mock_resolve.return_value = None
        resolver = DNSResolver()
        self.assertIsNone(resolver.resolve("google.com"))

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_no_match(self, mock_resolve: Mock) -> None:
        mock_answer = Mock()
        mock_answer.rrset = Mock()
        mock_answer.rrset.__str__ = Mock(return_value="google.com. 300 IN A abc")
        mock_resolve.return_value = mock_answer
        resolver = DNSResolver()
        self.assertIsNone(resolver.resolve("google.com"))

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_dns_exceptions(self, mock_resolve: Mock) -> None:
        from dns.resolver import NXDOMAIN, NoAnswer
        from dns.exception import Timeout
        import dns.name
        resolver = DNSResolver()
        for exc in [NXDOMAIN(qnames=[dns.name.from_text('google.com')]), Timeout(), NoAnswer()]:
            mock_resolve.side_effect = exc
            self.assertIsNone(resolver.resolve("google.com"))

    def test_reverse_resolve_invalid_type(self) -> None:
        resolver = DNSResolver()
        from ats_utilities.exceptions.ats_type_error import ATSTypeError
        with self.assertRaises(ATSTypeError):
            resolver.reverse_resolve(123)

    def test_reverse_resolve_empty(self) -> None:
        resolver = DNSResolver()
        from ats_utilities.exceptions.ats_value_error import ATSValueError
        with self.assertRaises(ATSValueError):
            resolver.reverse_resolve("")

    @patch('socket.gethostbyaddr')
    def test_reverse_resolve_herror(self, mock_gethostbyaddr: Mock) -> None:
        import socket
        mock_gethostbyaddr.side_effect = socket.herror()
        resolver = DNSResolver()
        self.assertIsNone(resolver.reverse_resolve("8.8.8.8"))

    def test_resolve_record_invalid_type_domain(self) -> None:
        resolver = DNSResolver()
        from ats_utilities.exceptions.ats_type_error import ATSTypeError
        with self.assertRaises(ATSTypeError):
            resolver.resolve_record(123, "A")

    def test_resolve_record_empty_domain(self) -> None:
        resolver = DNSResolver()
        from ats_utilities.exceptions.ats_value_error import ATSValueError
        with self.assertRaises(ATSValueError):
            resolver.resolve_record("", "A")

    def test_resolve_record_invalid_type_record(self) -> None:
        resolver = DNSResolver()
        from ats_utilities.exceptions.ats_type_error import ATSTypeError
        with self.assertRaises(ATSTypeError):
            resolver.resolve_record("google.com", 123)

    def test_resolve_record_empty_record(self) -> None:
        resolver = DNSResolver()
        from ats_utilities.exceptions.ats_value_error import ATSValueError
        with self.assertRaises(ATSValueError):
            resolver.resolve_record("google.com", "")

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_record_dns_exceptions(self, mock_resolve: Mock) -> None:
        from dns.resolver import NXDOMAIN, NoAnswer
        from dns.exception import Timeout
        import dns.name
        resolver = DNSResolver()
        for exc in [NXDOMAIN(qnames=[dns.name.from_text('google.com')]), Timeout(), NoAnswer()]:
            mock_resolve.side_effect = exc
            self.assertEqual(resolver.resolve_record("google.com", "A"), [])

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_record_generic_exception(self, mock_resolve: Mock) -> None:
        mock_resolve.side_effect = RuntimeError("generic error")
        resolver = DNSResolver()
        self.assertEqual(resolver.resolve_record("google.com", "A"), [])
