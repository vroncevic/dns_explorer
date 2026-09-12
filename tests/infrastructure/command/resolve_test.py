# -*- coding: UTF-8 -*-

'''
Module
    resolve_test.py
Info
    Unit tests for ResolveCommandDefinition and ResolveCommandExecutor.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.exceptions import ATSValueError
from dns_explorer.infrastructure.command.resolve_command_definition import ResolveCommandDefinition
from dns_explorer.infrastructure.command.resolve_command_executor import ResolveCommandExecutor
from dns_explorer.core.model.resolved_domain import ResolvedDomain


class MockContextBundle:
    def __init__(self, checker=None, reporter=None, verbose=False):
        self.checker = checker or Mock()
        self.reporter = reporter or Mock()
        self.verbose = verbose


class MockService:
    def __init__(self, resolved_domain=None):
        self.resolved_domain = resolved_domain

    def check_dns(self, domain: str) -> ResolvedDomain | None:
        return self.resolved_domain


class TestResolveCommand(unittest.TestCase):
    def test_definition(self) -> None:
        definition = ResolveCommandDefinition()
        self.assertEqual(definition.name, 'resolve')
        self.assertEqual(definition.help_text, 'Query forward IP address and reverse DNS hostnames for a single domain')
        self.assertTrue(len(definition.options) > 0)
        self.assertTrue(isinstance(str(definition), str))

    def test_executor_init_fail(self) -> None:
        definition = ResolveCommandDefinition()
        with self.assertRaises(ATSValueError):
            ResolveCommandExecutor(definition, None)

    def test_executor_execute_success(self) -> None:
        definition = ResolveCommandDefinition()
        bundle = MockContextBundle()
        executor = ResolveCommandExecutor(definition, bundle)

        resolved = ResolvedDomain(domain="google.com", ip="142.251.143.238", reverse=["dns.google"])
        service = MockService(resolved)

        params = {
            "domain": "google.com",
            "verbose": "True"
        }

        result = executor.execute(params=params, service=service)
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["stdout"], "resolved google.com")
        self.assertEqual(executor.get_definition(), definition)
        self.assertTrue(isinstance(str(executor), str))

    def test_executor_execute_failure(self) -> None:
        definition = ResolveCommandDefinition()
        bundle = MockContextBundle()
        executor = ResolveCommandExecutor(definition, bundle)

        service = MockService(None)

        params = {
            "domain": "google.com",
            "verbose": "False"
        }

        result = executor.execute(params=params, service=service)
        self.assertEqual(result["returncode"], 1)
        self.assertEqual(result["stderr"], "resolution failed for google.com")
