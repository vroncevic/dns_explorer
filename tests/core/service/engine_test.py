# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
Info
    Unit tests for Service class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from dns_explorer.core.service.engine import Service
from dns_explorer.core.service.idns_resolver import IDNSResolver
from dns_explorer.core.model.models import ResolvedDomain, DNSRecord


class DummyDNSResolver:
    def resolve(self, domain: str) -> str | None:
        return None

    def reverse_resolve(self, ip: str) -> list[str] | None:
        return None

    def resolve_record(self, domain: str, record_type: str) -> list[str]:
        return []

    def is_initialized(self) -> bool:
        return True


class TestService(unittest.TestCase):
    def test_service_initialization_success(self) -> None:
        resolver = DummyDNSResolver()
        service = Service(resolver)
        self.assertEqual(service._dns_resolver, resolver)

    def test_service_initialization_value_error(self) -> None:
        with self.assertRaises(Exception):
            Service(None)

    def test_service_initialization_type_error(self) -> None:
        with self.assertRaises(Exception):
            Service("invalid_resolver")

    def test_service_explore(self) -> None:
        resolver = DummyDNSResolver()
        resolver.resolve = Mock(side_effect=lambda domain: "142.251.143.238" if "google.com" in domain else None)
        resolver.reverse_resolve = Mock(return_value=["dns.google"])

        service = Service(resolver)
        result = service.explore(domain="google.com", cluster=0)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0].domain, "www.google.com")
        self.assertEqual(result[0].ip, "142.251.143.238")
        self.assertEqual(result[0].reverse, ["dns.google"])

    def test_service_check_dns(self) -> None:
        resolver = DummyDNSResolver()
        resolver.resolve = Mock(return_value="142.251.143.238")
        resolver.reverse_resolve = Mock(return_value=["dns.google"])

        service = Service(resolver)
        res = service.check_dns(domain="google.com")
        self.assertIsNotNone(res)
        self.assertEqual(res.domain, "google.com")
        self.assertEqual(res.ip, "142.251.143.238")
        self.assertEqual(res.reverse, ["dns.google"])

    def test_service_get_records(self) -> None:
        resolver = DummyDNSResolver()
        resolver.resolve_record = Mock(return_value=["142.251.143.238"])

        service = Service(resolver)
        records = service.get_records(domain="google.com")
        self.assertIsInstance(records, list)

    def test_service_reverse_resolve(self) -> None:
        resolver = DummyDNSResolver()
        resolver.reverse_resolve = Mock(return_value=["dns.google"])

        service = Service(resolver)
        hosts = service.reverse_resolve(ip="8.8.8.8")
        self.assertEqual(hosts, ["dns.google"])

    def test_service_is_initialized(self) -> None:
        resolver = DummyDNSResolver()
        resolver.is_initialized = Mock(return_value=True)

        service = Service(resolver)
        self.assertTrue(service.is_initialized())
