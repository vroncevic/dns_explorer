# -*- coding: UTF-8 -*-

'''
Module
    records_test.py
Info
    Unit tests for RecordsCommandDefinition and RecordsCommandExecutor.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.exceptions import ATSValueError
from dns_explorer.infrastructure.command.records_command_definition import RecordsCommandDefinition
from dns_explorer.infrastructure.command.records_command_executor import RecordsCommandExecutor
from dns_explorer.core.model.models import DNSRecord


class MockContextBundle:
    def __init__(self, checker=None, reporter=None, verbose=False):
        self.checker = checker or Mock()
        self.reporter = reporter or Mock()
        self.verbose = verbose


class MockService:
    def __init__(self, records=None):
        self.records = records if records is not None else []

    def get_records(self, domain: str) -> list[DNSRecord]:
        return self.records


class TestRecordsCommand(unittest.TestCase):
    def test_definition(self) -> None:
        definition = RecordsCommandDefinition()
        self.assertEqual(definition.name, 'records')
        self.assertEqual(definition.help_text, 'Query various DNS records (A, AAAA, MX, TXT, NS, SOA) for a domain')
        self.assertTrue(len(definition.options) > 0)
        self.assertTrue(isinstance(str(definition), str))

    def test_executor_init_fail(self) -> None:
        definition = RecordsCommandDefinition()
        with self.assertRaises(ATSValueError):
            RecordsCommandExecutor(definition, None)

    def test_executor_execute_success(self) -> None:
        definition = RecordsCommandDefinition()
        bundle = MockContextBundle()
        executor = RecordsCommandExecutor(definition, bundle)

        records = [
            DNSRecord(record_type="A", value="142.251.143.238"),
            DNSRecord(record_type="MX", value="10 mail.google.com")
        ]
        service = MockService(records)

        params = {
            "domain": "google.com"
        }

        result = executor.execute(params=params, service=service)
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["stdout"], "records done")
        self.assertEqual(executor.get_definition(), definition)
        self.assertTrue(isinstance(str(executor), str))
