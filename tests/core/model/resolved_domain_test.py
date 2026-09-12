# -*- coding: UTF-8 -*-

'''
Module
    resolved_domain_test.py
Info
    Unit tests for ResolvedDomain model class.
'''

from __future__ import annotations

from unittest import TestCase

from dns_explorer.core.model.resolved_domain import ResolvedDomain


class TestResolvedDomain(TestCase):
    def test_resolved_domain_initialization_with_list(self) -> None:
        domain = "google.com"
        ip = "142.251.143.238"
        reverse_list = ["dns.google"]
        res = ResolvedDomain(domain=domain, ip=ip, reverse=reverse_list)
        self.assertEqual(res.domain, domain)
        self.assertEqual(res.ip, ip)
        self.assertEqual(res.reverse, ("dns.google",))
        self.assertIsInstance(res.reverse, tuple)

    def test_resolved_domain_initialization_with_tuple(self) -> None:
        domain = "example.com"
        ip = "93.184.216.34"
        reverse_tuple = ("example.org", "example.net")
        res = ResolvedDomain(domain=domain, ip=ip, reverse=reverse_tuple)
        self.assertEqual(res.domain, domain)
        self.assertEqual(res.ip, ip)
        self.assertEqual(res.reverse, reverse_tuple)
        self.assertIsInstance(res.reverse, tuple)
