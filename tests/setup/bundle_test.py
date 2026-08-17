# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
Info
    Unit tests for DNSExplorerBundle class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.base.setup.bundle import BaseBundle

from dns_explorer.core.service.iservice import IService
from dns_explorer.core.service.idns_resolver import IDNSResolver
from dns_explorer.infrastructure.cli.icli import ICLI
from dns_explorer.setup.bundle import DNSExplorerBundle


class TestDNSExplorerBundle(unittest.TestCase):

    def test_bundle_creation_and_to_dict(self) -> None:
        mock_base = Mock(spec=BaseBundle)
        mock_service = Mock(spec=IService)
        mock_dns_resolver = Mock(spec=IDNSResolver)
        mock_cli = Mock(spec=ICLI)

        bundle = DNSExplorerBundle(
            base=mock_base,
            service=mock_service,
            dns_resolver=mock_dns_resolver,
            cli=mock_cli
        )

        self.assertEqual(bundle.base, mock_base)
        self.assertEqual(bundle.service, mock_service)
        self.assertEqual(bundle.dns_resolver, mock_dns_resolver)
        self.assertEqual(bundle.cli, mock_cli)

        bundle_dict = bundle.to_dict()
        self.assertIsInstance(bundle_dict, dict)
