# -*- coding: UTF-8 -*-

'''
Module
    models_test.py
Info
    Unit tests for ResolvedDomain and DNSRecord classes.
'''

from __future__ import annotations

from unittest import TestCase

from dns_explorer.core.model.dns_record import DNSRecord
from dns_explorer.core.model.resolved_domain import ResolvedDomain


class TestModels(TestCase):
    def test_resolved_domain_initialization(self) -> None:
        domain = "google.com"
        ip = "142.251.143.238"
        reverse = ["dns.google"]
        res = ResolvedDomain(domain=domain, ip=ip, reverse=reverse)
        self.assertEqual(res.domain, domain)
        self.assertEqual(res.ip, ip)
        self.assertEqual(res.reverse, ("dns.google",))

    def test_dns_record_initialization(self) -> None:
        record_type = "A"
        value = "142.251.143.238"
        rec = DNSRecord(record_type=record_type, value=value)
        self.assertEqual(rec.record_type, record_type)
        self.assertEqual(rec.value, value)
