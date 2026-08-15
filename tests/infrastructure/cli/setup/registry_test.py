# -*- coding: UTF-8 -*-

'''
Module
    registry_test.py
Info
    Unit tests for CLIBundleRegistry class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from dns_explorer.core.service.iservice import IService
from dns_explorer.infrastructure.cli.setup.bundle import CLIBundle
from dns_explorer.infrastructure.cli.setup.registry import CLIBundleRegistry


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


class TestCLIBundleRegistry(unittest.TestCase):

    def test_create_bundle_success(self) -> None:
        mock_service = DummyService()
        mock_parser = Mock(spec=IOptionManager)

        dependencies = {
            'service': mock_service,
            'parser': mock_parser,
            'commands': []
        }
        bundle = CLIBundleRegistry.create_bundle(dependencies)
        self.assertIsInstance(bundle, CLIBundle)
        self.assertEqual(bundle.service, mock_service)
        self.assertEqual(bundle.parser, mock_parser)

    def test_create_bundle_invalid_dependencies(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleRegistry.create_bundle(None)

    def test_get_version(self) -> None:
        self.assertEqual(CLIBundleRegistry.get_version(), '1.0.6')
