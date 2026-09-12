# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
Info
    Unit tests for DNSExplorerBundleFactory class.
'''

from __future__ import annotations

import unittest

from dns_explorer.setup.bundle import DNSExplorerBundle
from dns_explorer.setup.factory import DNSExplorerBundleFactory


class TestDNSExplorerBundleFactory(unittest.TestCase):

    def test_create_bundle_default(self) -> None:
        bundle = DNSExplorerBundleFactory.create_bundle()
        self.assertIsInstance(bundle, DNSExplorerBundle)

    def test_create_bundle_with_options(self) -> None:
        options = {'info_file': 'dns_explorer/infrastructure/config/dns_explorer.cfg'}
        bundle = DNSExplorerBundleFactory.create_bundle(options)
        self.assertIsInstance(bundle, DNSExplorerBundle)

    def test_create_bundle_invalid_options(self) -> None:
        options = {'info_file': 123}
        with self.assertRaises(Exception):
            DNSExplorerBundleFactory.create_bundle(options)

    def test_get_version(self) -> None:
        self.assertEqual(DNSExplorerBundleFactory.get_version(), '1.0.7')

