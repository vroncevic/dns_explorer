# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
Info
    Unit tests for CLIBundleFactory class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from dns_explorer.infrastructure.cli.setup.bundle import CLIBundle
from dns_explorer.infrastructure.cli.setup.factory import CLIBundleFactory


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


class TestCLIBundleFactory(unittest.TestCase):

    def test_create_bundle_success(self) -> None:
        mock_service = DummyService()
        mock_parser = Mock(spec=IOptionManager)

        from ats_utilities.context.factory import ContextBundleFactory
        mock_context_bundle = ContextBundleFactory.create_bundle()
        options = {
            'service': mock_service,
            'parser': mock_parser,
            'context_bundle': mock_context_bundle
        }
        bundle = CLIBundleFactory.create_bundle(options)
        self.assertIsInstance(bundle, CLIBundle)

    def test_get_version(self) -> None:
        self.assertEqual(CLIBundleFactory.get_version(), '1.0.7')

