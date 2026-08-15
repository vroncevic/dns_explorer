# -*- coding: UTF-8 -*-

'''
Module
    keys_test.py
Info
    Unit tests for DNSExplorerBundleKeys class.
'''

from __future__ import annotations

import unittest
from types import MappingProxyType

from dns_explorer.setup.keys import DNSExplorerBundleKeys


class TestDNSExplorerBundleKeys(unittest.TestCase):

    def test_get_dependency_to_type(self) -> None:
        deps = DNSExplorerBundleKeys.get_dependency_to_type()
        self.assertIsInstance(deps, MappingProxyType)
        self.assertIn(DNSExplorerBundleKeys.DEPENDENCY_BASE, deps)
        self.assertIn(DNSExplorerBundleKeys.DEPENDENCY_SERVICE, deps)
        self.assertIn(DNSExplorerBundleKeys.DEPENDENCY_DNS_RESOLVER, deps)
        self.assertIn(DNSExplorerBundleKeys.DEPENDENCY_CLI, deps)

    def test_get_option_to_type(self) -> None:
        opts = DNSExplorerBundleKeys.get_option_to_type()
        self.assertIsInstance(opts, MappingProxyType)
        self.assertIn(DNSExplorerBundleKeys.OPTION_INFO_FILE, opts)
