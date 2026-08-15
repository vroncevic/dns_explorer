# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
Info
    Unit tests for DNSExplorerBundleValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.base.setup.bundle import BaseBundle

from dns_explorer.core.service.iservice import IService
from dns_explorer.core.service.idns_resolver import IDNSResolver
from dns_explorer.infrastructure.cli.icli import ICLI
from dns_explorer.setup.bundle import DNSExplorerBundle
from dns_explorer.setup.validator import DNSExplorerBundleValidator


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


class TestDNSExplorerBundleValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_dns_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI()

        bundle = DNSExplorerBundle(
            base=mock_base,
            service=dummy_service,
            dns_resolver=dummy_dns_resolver,
            cli=dummy_cli
        )

        DNSExplorerBundleValidator.validate(bundle)

    def test_validate_bundle_none(self) -> None:
        with self.assertRaises(Exception):
            DNSExplorerBundleValidator.validate(None)

    def test_validate_bundle_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            DNSExplorerBundleValidator.validate("invalid_bundle")

    def test_validate_missing_components(self) -> None:
        dummy_service = DummyService()
        dummy_dns_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI()

        with self.assertRaises(Exception):
            bundle = DNSExplorerBundle(
                base=None,
                service=dummy_service,
                dns_resolver=dummy_dns_resolver,
                cli=dummy_cli
            )
            DNSExplorerBundleValidator.validate(bundle)

    def test_validate_invalid_component_types(self) -> None:
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_dns_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI()

        with self.assertRaises(Exception):
            bundle = DNSExplorerBundle(
                base="invalid",
                service=dummy_service,
                dns_resolver=dummy_dns_resolver,
                cli=dummy_cli
            )
            DNSExplorerBundleValidator.validate(bundle)

        with self.assertRaises(Exception):
            bundle = DNSExplorerBundle(
                base=mock_base,
                service="invalid",
                dns_resolver=dummy_dns_resolver,
                cli=dummy_cli
            )
            DNSExplorerBundleValidator.validate(bundle)
        with self.assertRaises(Exception):
            bundle = DNSExplorerBundle(
                base=mock_base,
                service=dummy_service,
                dns_resolver="invalid",
                cli=dummy_cli
            )
            DNSExplorerBundleValidator.validate(bundle)

            DNSExplorerBundleValidator.validate(bundle)

    def test_is_valid_success(self) -> None:
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_dns_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI()

        bundle = DNSExplorerBundle(
            base=mock_base,
            service=dummy_service,
            dns_resolver=dummy_dns_resolver,
            cli=dummy_cli
        )
        self.assertTrue(DNSExplorerBundleValidator.is_valid(bundle))

    def test_is_valid_failure(self) -> None:
        self.assertFalse(DNSExplorerBundleValidator.is_valid(None))
        self.assertFalse(DNSExplorerBundleValidator.is_valid("invalid"))

