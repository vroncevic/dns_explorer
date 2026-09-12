# -*- coding: UTF-8 -*-

'''
Module
    explore_test.py
Info
    Unit tests for ExploreCommandDefinition and ExploreCommandExecutor.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.exceptions import ATSValueError
from dns_explorer.infrastructure.command.explore_command_definition import ExploreCommandDefinition
from dns_explorer.infrastructure.command.explore_command_executor import ExploreCommandExecutor
from dns_explorer.core.model.resolved_domain import ResolvedDomain


class MockContextBundle:
    def __init__(self, checker=None, reporter=None, verbose=False):
        self.checker = checker or Mock()
        self.reporter = reporter or Mock()
        self.verbose = verbose


class MockService:
    def __init__(self, resolved_domains=None):
        self.resolved_domains = resolved_domains if resolved_domains is not None else []

    def explore(self, domain: str, cluster: int) -> list[ResolvedDomain]:
        return self.resolved_domains


class TestExploreCommand(unittest.TestCase):
    def test_definition(self) -> None:
        definition = ExploreCommandDefinition()
        self.assertEqual(definition.name, 'explore')
        self.assertEqual(definition.help_text, 'DNS exploration command')
        self.assertTrue(len(definition.options) > 0)
        self.assertTrue(isinstance(str(definition), str))

    def test_executor_init_fail(self) -> None:
        definition = ExploreCommandDefinition()
        with self.assertRaises(ATSValueError):
            ExploreCommandExecutor(definition, None)

    def test_executor_execute_success(self) -> None:
        definition = ExploreCommandDefinition()
        bundle = MockContextBundle()
        executor = ExploreCommandExecutor(definition, bundle)

        resolved = [
            ResolvedDomain(domain="www.google.com", ip="142.251.143.238", reverse=["dns.google"])
        ]
        service = MockService(resolved)

        params = {
            "domain": "google.com",
            "cluster": "0",
            "verbose": "False"
        }

        result = executor.execute(params=params, service=service)
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["stdout"], "explore done")
        self.assertEqual(executor.get_definition(), definition)
        self.assertTrue(isinstance(str(executor), str))

    def test_executor_execute_verbose(self) -> None:
        definition = ExploreCommandDefinition()
        bundle = MockContextBundle()
        executor = ExploreCommandExecutor(definition, bundle)

        resolved = [
            ResolvedDomain(domain="www.google.com", ip="142.251.143.238", reverse=["dns.google"])
        ]
        service = MockService(resolved)

        params = {
            "domain": "google.com",
            "cluster": "1",
            "verbose": "True"
        }

        result = executor.execute(params=params, service=service)
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["stdout"], "explore done")
