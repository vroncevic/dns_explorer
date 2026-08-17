# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
Info
    Unit tests for CLIBundleValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from dns_explorer.core.service.iservice import IService
from dns_explorer.infrastructure.cli.setup.bundle import CLIBundle
from dns_explorer.infrastructure.cli.setup.validator import CLIBundleValidator


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


class TestCLIBundleValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        mock_service = DummyService()
        mock_parser = Mock(spec=IOptionManager)
        bundle = CLIBundle(
            service=mock_service,
            parser=mock_parser,
            commands=[]
        )
        CLIBundleValidator.validate(bundle)

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleValidator.validate(None)

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleValidator.validate("invalid")

    def test_is_valid_success(self) -> None:
        mock_service = DummyService()
        mock_parser = Mock(spec=IOptionManager)
        bundle = CLIBundle(
            service=mock_service,
            parser=mock_parser,
            commands=[]
        )
        self.assertTrue(CLIBundleValidator.is_valid(bundle))

    def test_is_valid_failure(self) -> None:
        self.assertFalse(CLIBundleValidator.is_valid(None))
        self.assertFalse(CLIBundleValidator.is_valid("invalid"))
