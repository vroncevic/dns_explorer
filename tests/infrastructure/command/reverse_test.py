# -*- coding: UTF-8 -*-

'''
Module
    reverse_test.py
Info
    Unit tests for ReverseCommandDefinition and ReverseCommandExecutor.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.exceptions import ATSValueError
from dns_explorer.infrastructure.command.reverse_command_definition import ReverseCommandDefinition
from dns_explorer.infrastructure.command.reverse_command_executor import ReverseCommandExecutor


class MockContextBundle:
    def __init__(self, checker=None, reporter=None, verbose=False):
        self.checker = checker or Mock()
        self.reporter = reporter or Mock()
        self.verbose = verbose


class MockService:
    def __init__(self, hostnames=None):
        self.hostnames = hostnames if hostnames is not None else []

    def reverse_resolve(self, ip: str) -> list[str]:
        return self.hostnames


class TestReverseCommand(unittest.TestCase):
    def test_definition(self) -> None:
        definition = ReverseCommandDefinition()
        self.assertEqual(definition.name, 'reverse')
        self.assertEqual(definition.help_text, 'Query reverse DNS hostnames for an IP address')
        self.assertTrue(len(definition.options) > 0)
        self.assertTrue(isinstance(str(definition), str))

    def test_executor_init_fail(self) -> None:
        definition = ReverseCommandDefinition()
        with self.assertRaises(ATSValueError):
            ReverseCommandExecutor(definition, None)

    def test_executor_execute_success(self) -> None:
        definition = ReverseCommandDefinition()
        bundle = MockContextBundle()
        executor = ReverseCommandExecutor(definition, bundle)

        service = MockService(["dns.google"])

        params = {
            "ip": "8.8.8.8"
        }

        result = executor.execute(params=params, service=service)
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["stdout"], "reverse resolved 8.8.8.8")
        self.assertEqual(executor.get_definition(), definition)
        self.assertTrue(isinstance(str(executor), str))

    def test_executor_execute_failure(self) -> None:
        definition = ReverseCommandDefinition()
        bundle = MockContextBundle()
        executor = ReverseCommandExecutor(definition, bundle)

        service = MockService([])

        params = {
            "ip": "8.8.8.8"
        }

        result = executor.execute(params=params, service=service)
        self.assertEqual(result["returncode"], 1)
        self.assertEqual(result["stderr"], "no hostnames found for 8.8.8.8")
