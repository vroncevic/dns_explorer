# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
Info
    Unit tests for DNSExplorer engine.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.exceptions import ATSValueError

from dns_explorer.engine import DNSExplorer
from dns_explorer.setup.bundle import DNSExplorerBundle
from dns_explorer.setup.factory import DNSExplorerBundleFactory
from dns_explorer.core.model.dns_record import DNSRecord
from dns_explorer.core.model.resolved_domain import ResolvedDomain


class DummyService:
    def explore(self, domain: str, cluster: int = 0) -> list[ResolvedDomain]:
        return []

    def check_dns(self, domain: str) -> ResolvedDomain | None:
        return None

    def get_records(self, domain: str) -> list[DNSRecord]:
        return []

    def reverse_resolve(self, ip: str) -> list[str]:
        return []

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummyService'


class DummyDNSResolver:
    def resolve(self, domain: str) -> str | None:
        return '142.251.143.238'

    def reverse_resolve(self, ip: str) -> list[str] | None:
        return ['dns.google']

    def resolve_record(self, domain: str, record_type: str) -> list[str]:
        return []

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummyDNSResolver'


class DummyCLI:
    def __init__(self, return_code: int = 0, stderr: str = '') -> None:
        self.return_code = return_code
        self.stderr = stderr

    def run(self) -> dict[str, object]:
        return {'returncode': self.return_code, 'stderr': self.stderr}

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummyCLI'


class TestDNSExplorer(unittest.TestCase):
    def test_engine_init_success(self) -> None:
        bundle = DNSExplorerBundleFactory.create_bundle()
        engine = DNSExplorer(bundle)
        self.assertTrue(engine.is_initialized())

    def test_engine_init_fail_validation(self) -> None:
        engine = DNSExplorer(None)
        self.assertFalse(engine.is_initialized())

    def test_engine_process_success(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='dns_explorer/infrastructure/config/dns_explorer.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI(return_code=0)

        bundle = DNSExplorerBundle(
            base=mock_base,
            service=dummy_service,
            dns_resolver=dummy_resolver,
            cli=dummy_cli
        )

        engine = DNSExplorer(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertTrue(engine.process())

    def test_engine_process_cli_failure(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='dns_explorer/infrastructure/config/dns_explorer.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI(return_code=1, stderr='CLI error')

        bundle = DNSExplorerBundle(
            base=mock_base,
            service=dummy_service,
            dns_resolver=dummy_resolver,
            cli=dummy_cli
        )

        engine = DNSExplorer(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_not_initialized(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='dns_explorer/infrastructure/config/dns_explorer.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI()

        mock_base.option_manager.is_initialized = Mock(return_value=False)

        bundle = DNSExplorerBundle(
            base=mock_base,
            service=dummy_service,
            dns_resolver=dummy_resolver,
            cli=dummy_cli
        )

        engine = DNSExplorer(bundle)
        self.assertFalse(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_exception(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='dns_explorer/infrastructure/config/dns_explorer.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_resolver = DummyDNSResolver()

        dummy_cli = DummyCLI()
        dummy_cli.run = Mock(side_effect=Exception('Unexpected error'))

        bundle = DNSExplorerBundle(
            base=mock_base,
            service=dummy_service,
            dns_resolver=dummy_resolver,
            cli=dummy_cli
        )

        engine = DNSExplorer(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_validation_exception(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='dns_explorer/infrastructure/config/dns_explorer.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI()
        dummy_cli.run = Mock(side_effect=ATSValueError('Validation error in run'))

        bundle = DNSExplorerBundle(
            base=mock_base,
            service=dummy_service,
            dns_resolver=dummy_resolver,
            cli=dummy_cli
        )

        engine = DNSExplorer(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    @patch('dns_explorer.setup.validator.DNSExplorerBundleValidator.validate')
    def test_engine_init_generic_exception(self, mock_validate: Mock) -> None:
        mock_validate.side_effect = Exception('Unexpected generic validation error')

        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='dns_explorer/infrastructure/config/dns_explorer.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_resolver = DummyDNSResolver()
        dummy_cli = DummyCLI()

        bundle = DNSExplorerBundle(
            base=mock_base,
            service=dummy_service,
            dns_resolver=dummy_resolver,
            cli=dummy_cli
        )

        engine = DNSExplorer(bundle)
        self.assertFalse(engine.is_initialized())
