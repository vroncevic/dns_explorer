# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
Info
    Unit tests for DNSExplorerBundleDependenciesValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.base.setup.bundle import BaseBundle

from dns_explorer.setup.dep_validator import DNSExplorerBundleDependenciesValidator


class DummyService:

    def explore(self, domain: str, cluster: int = 0, verbose: bool = False) -> list[object]:
        return []

    def check_dns(self, domain: str, verbose: bool = False) -> object:
        return None

    def get_records(self, domain: str) -> list[object]:
        return []

    def reverse_resolve(self, ip: str) -> list[str]:
        return []

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummyService'


class DummyDNSResolver:

    def resolve(self, domain: str) -> str | None:
        return None

    def reverse_resolve(self, ip: str) -> list[str] | None:
        return None

    def resolve_record(self, domain: str, record_type: str) -> list[str]:
        return []

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummyDNSResolver'


class DummyCLI:

    def run(self) -> dict[str, object]:
        return {}

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummyCLI'


class TestDNSExplorerBundleDependenciesValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_dns_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI()

        dependencies = {
            'base': mock_base,
            'service': dummy_service,
            'dns_resolver': dummy_dns_resolver,
            'cli': dummy_cli
        }
        DNSExplorerBundleDependenciesValidator.validate(dependencies)

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            DNSExplorerBundleDependenciesValidator.validate(None)

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            DNSExplorerBundleDependenciesValidator.validate("not_a_mapping")

    def test_validate_missing_dependency(self) -> None:
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_dns_resolver = DummyDNSResolver()

        dependencies = {
            'base': mock_base,
            'service': dummy_service,
            'dns_resolver': dummy_dns_resolver
        }
        with self.assertRaises(Exception):
            DNSExplorerBundleDependenciesValidator.validate(dependencies)

    def test_is_valid_success(self) -> None:
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_dns_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI()

        dependencies = {
            'base': mock_base,
            'service': dummy_service,
            'dns_resolver': dummy_dns_resolver,
            'cli': dummy_cli
        }
        self.assertTrue(DNSExplorerBundleDependenciesValidator.is_valid(dependencies))

    def test_is_valid_failure(self) -> None:
        self.assertFalse(DNSExplorerBundleDependenciesValidator.is_valid(None))
        self.assertFalse(DNSExplorerBundleDependenciesValidator.is_valid("not_a_mapping"))
        dependencies = {
            'base': Mock(spec=BaseBundle),
            'service': DummyService(),
            'dns_resolver': DummyDNSResolver()
        }
        self.assertFalse(DNSExplorerBundleDependenciesValidator.is_valid(dependencies))
