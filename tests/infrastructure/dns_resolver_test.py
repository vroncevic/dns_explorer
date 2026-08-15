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
