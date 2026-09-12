# -*- coding: UTF-8 -*-

'''
Module
    registry_test.py
Info
    Unit tests for DNSExplorerBundleRegistry class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.base.setup.bundle import BaseBundle

from dns_explorer.core.service.iservice import IService
from dns_explorer.core.service.idns_resolver import IDNSResolver
from dns_explorer.infrastructure.cli.icli import ICLI
from dns_explorer.setup.bundle import DNSExplorerBundle
from dns_explorer.setup.registry import DNSExplorerBundleRegistry


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


class TestDNSExplorerBundleRegistry(unittest.TestCase):

    def test_create_bundle_success(self) -> None:
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
        
        bundle = DNSExplorerBundleRegistry.create_bundle(dependencies)
        self.assertIsInstance(bundle, DNSExplorerBundle)
        self.assertEqual(bundle.base, mock_base)

    def test_create_bundle_invalid_dependencies(self) -> None:
        with self.assertRaises(Exception):
            DNSExplorerBundleRegistry.create_bundle(None)

    def test_get_version(self) -> None:
        self.assertEqual(DNSExplorerBundleRegistry.get_version(), '1.0.7')

