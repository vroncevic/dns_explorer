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
        result = service.explore(domain="google.com", cluster=1)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 31)
        self.assertEqual(result[0].domain, "www.google.com")
        self.assertEqual(result[0].ip, "142.251.143.238")
        self.assertEqual(result[0].reverse, ("dns.google",))

    def test_service_check_dns(self) -> None:
        resolver = DummyDNSResolver()
        resolver.resolve = Mock(return_value="142.251.143.238")
        resolver.reverse_resolve = Mock(return_value=["dns.google"])

        service = Service(resolver)
        res = service.check_dns(domain="google.com")
        self.assertIsNotNone(res)
        self.assertEqual(res.domain, "google.com")
        self.assertEqual(res.ip, "142.251.143.238")
        self.assertEqual(res.reverse, ("dns.google",))

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

    def test_service_explore_empty_domain(self) -> None:
        resolver = DummyDNSResolver()
        service = Service(resolver)
        with self.assertRaises(ValueError):
            service.explore(domain="", cluster=0)

    def test_service_get_records_empty_domain(self) -> None:
        resolver = DummyDNSResolver()
        service = Service(resolver)
        with self.assertRaises(ValueError):
            service.get_records(domain="")

    def test_service_reverse_resolve_empty_ip(self) -> None:
        resolver = DummyDNSResolver()
        service = Service(resolver)
        with self.assertRaises(ValueError):
            service.reverse_resolve(ip="")

    def test_service_check_dns_exception(self) -> None:
        resolver = DummyDNSResolver()
        resolver.resolve = Mock(side_effect=Exception("resolve error"))
        service = Service(resolver)
        res = service.check_dns(domain="google.com")
        self.assertIsNone(res)

    def test_service_get_records_exception(self) -> None:
        resolver = DummyDNSResolver()
        resolver.resolve_record = Mock(side_effect=Exception("resolve_record error"))
        service = Service(resolver)
        records = service.get_records(domain="google.com")
        self.assertEqual(records, [])

    def test_service_reverse_resolve_exception(self) -> None:
        resolver = DummyDNSResolver()
        resolver.reverse_resolve = Mock(side_effect=Exception("reverse_resolve error"))
        service = Service(resolver)
        hosts = service.reverse_resolve(ip="8.8.8.8")
        self.assertEqual(hosts, [])

    def test_service_check_dns_none_reverse(self) -> None:
        resolver = DummyDNSResolver()
        resolver.resolve = Mock(return_value="142.251.143.238")
        resolver.reverse_resolve = Mock(return_value=None)
        service = Service(resolver)
        res = service.check_dns(domain="google.com")
        self.assertIsNone(res)
