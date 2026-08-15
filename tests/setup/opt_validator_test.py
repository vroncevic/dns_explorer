# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
Info
    Unit tests for DNSExplorerBundleOptionsValidator class.
'''

from __future__ import annotations

import unittest

from dns_explorer.setup.opt_validator import DNSExplorerBundleOptionsValidator


class TestDNSExplorerBundleOptionsValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        options = {'info_file': 'some_path'}
        DNSExplorerBundleOptionsValidator.validate(options)

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            DNSExplorerBundleOptionsValidator.validate(None)

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            DNSExplorerBundleOptionsValidator.validate("not_a_mapping")

            options = {'info_file': 123}
            DNSExplorerBundleOptionsValidator.validate(options)

    def test_is_valid_success(self) -> None:
        options = {'info_file': 'some_path'}
        self.assertTrue(DNSExplorerBundleOptionsValidator.is_valid(options))

    def test_is_valid_failure(self) -> None:
        self.assertFalse(DNSExplorerBundleOptionsValidator.is_valid(None))
        self.assertFalse(DNSExplorerBundleOptionsValidator.is_valid("not_a_mapping"))
        self.assertFalse(DNSExplorerBundleOptionsValidator.is_valid({'info_file': 123}))

