# -*- coding: UTF-8 -*-

'''
Module
    dns_record_test.py
Info
    Unit tests for DNSRecord model class.
'''

from __future__ import annotations

from unittest import TestCase

from dns_explorer.core.model.dns_record import DNSRecord


class TestDNSRecord(TestCase):
    def test_dns_record_initialization(self) -> None:
        record_type = "A"
        value = "142.251.143.238"
        rec = DNSRecord(record_type=record_type, value=value)
        self.assertEqual(rec.record_type, record_type)
        self.assertEqual(rec.value, value)
