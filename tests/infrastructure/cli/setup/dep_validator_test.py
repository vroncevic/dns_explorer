# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
Info
    Unit tests for CLIBundleDependenciesValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from dns_explorer.core.service.iservice import IService
from dns_explorer.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator


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


class TestCLIBundleDependenciesValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        mock_service = DummyService()
        mock_parser = Mock(spec=IOptionManager)

        dependencies = {
            'service': mock_service,
            'parser': mock_parser,
            'commands': []
        }
        CLIBundleDependenciesValidator.validate(dependencies)

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleDependenciesValidator.validate(None)

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleDependenciesValidator.validate("invalid")

    def test_validate_missing_dependency(self) -> None:
        mock_service = DummyService()
        dependencies = {
            'service': mock_service
        }
        with self.assertRaises(Exception):
            CLIBundleDependenciesValidator.validate(dependencies)

    def test_is_valid_success(self) -> None:
        mock_service = DummyService()
        mock_parser = Mock(spec=IOptionManager)

        dependencies = {
            'service': mock_service,
            'parser': mock_parser,
            'commands': []
        }
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(dependencies))

    def test_is_valid_failure(self) -> None:
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(None))
        self.assertFalse(CLIBundleDependenciesValidator.is_valid("invalid"))
        dependencies = {
            'service': DummyService()
        }
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(dependencies))
