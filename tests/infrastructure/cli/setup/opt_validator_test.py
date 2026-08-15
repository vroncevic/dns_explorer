# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
Info
    Unit tests for CLIBundleOptionsValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from dns_explorer.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator


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


class TestCLIBundleOptionsValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        mock_service = DummyService()
        mock_parser = Mock(spec=IOptionManager)

        from ats_utilities.context.factory import ContextBundleFactory
        mock_context_bundle = ContextBundleFactory.create_bundle()
        options = {
            'service': mock_service,
            'parser': mock_parser,
            'context_bundle': mock_context_bundle
        }
        CLIBundleOptionsValidator.validate(options)

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleOptionsValidator.validate(None)

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleOptionsValidator.validate("invalid")

    def test_validate_missing_option(self) -> None:
        mock_service = DummyService()
        options = {
            'service': mock_service
        }
        with self.assertRaises(Exception):
            CLIBundleOptionsValidator.validate(options)

        with self.assertRaises(Exception):
            CLIBundleOptionsValidator.validate(options)

    def test_is_valid_success(self) -> None:
        mock_service = DummyService()
        mock_parser = Mock(spec=IOptionManager)

        from ats_utilities.context.factory import ContextBundleFactory
        mock_context_bundle = ContextBundleFactory.create_bundle()
        options = {
            'service': mock_service,
            'parser': mock_parser,
            'context_bundle': mock_context_bundle
        }
        self.assertTrue(CLIBundleOptionsValidator.is_valid(options))

    def test_is_valid_failure(self) -> None:
        self.assertFalse(CLIBundleOptionsValidator.is_valid(None))
        self.assertFalse(CLIBundleOptionsValidator.is_valid("invalid"))
        options = {
            'service': DummyService()
        }
        self.assertFalse(CLIBundleOptionsValidator.is_valid(options))

