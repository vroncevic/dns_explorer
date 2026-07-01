# -*- coding: UTF-8 -*-

'''
Module
    test_infrastructure.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    dns_explorer is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    dns_explorer is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for infrastructure adapters.
'''

import unittest
from unittest.mock import patch, MagicMock
from typing import Any
from ats_utilities.option.engine import OptionManager
from ats_utilities.option.component_bundle import OptionComponentBundle
from ats_utilities.context_bundle import ContextBundle
from ats_utilities.checker.engine import Checker
from ats_utilities.reporter.engine import Reporter
from ats_utilities.option.command_option import CommandOption
from ats_utilities.option.ioption_parser import IOptionManager
from dns_explorer.infrastructure.icli_command import ICLICommand
from dns_explorer.infrastructure.cli_bundle import CLIBundle
from dns_explorer.infrastructure.cli import CLI
from dns_explorer.domain.ports.iservice import IService
from dns_explorer.infrastructure.dns_resolver import DNSResolver
from dns_explorer.infrastructure.explore_command import ExploreCommand
from dns_explorer.infrastructure.records_command import RecordsCommand
from dns_explorer.infrastructure.resolve_command import ResolveCommand
from dns_explorer.infrastructure.reverse_command import ReverseCommand
from dns_explorer.domain.models import ResolvedDomain, DNSRecord

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class DummyCommand(ICLICommand):
    '''
        Dummy CLI command for testing ArgParser.

        It defines:

            :attributes: None.
            :methods:
                | name - Command name.
                | help_text - Command help text.
                | options - Command options.
                | execute - Simulates command execution.
    '''

    @property
    def name(self) -> str:
        '''
            Returns command name.

            :return: The command name.
            :rtype: <str>
            :exceptions: None.
        '''
        return "dummy"

    @property
    def help_text(self) -> str:
        '''
            Returns command help text.

            :return: The command help.
            :rtype: <str>
            :exceptions: None.
        '''
        return "Dummy command for tests"

    @property
    def options(self) -> list[CommandOption]:
        '''
            Returns command options.

            :return: List of command options.
            :rtype: <List[CommandOption]>
            :exceptions: None.
        '''
        return [
            CommandOption(name="--foo", help_text="foo parameter", default="bar"),
            CommandOption(name="--req", help_text="required parameter", required=True),
        ]

    def execute(self, params: dict, service: IService) -> None:
        '''
            Simulates execution.

            :param params: Execution params.
            :type params: <dict>
            :param service: Generation service.
            :type service: <IFileGen>
            :exceptions: None.
        '''
        pass

    def __str__(self) -> str:
        '''
            Returns the string representation of the command.

            :return: The string representation of the command.
            :rtype: <str>
            :exceptions: None.
        '''
        return f"DummyCommand(name='{self.name}', help_text='{self.help_text}', options={self.options})"


class TestInfrastructure(unittest.TestCase):
    '''
        Defines infrastructure adapters unit tests.

        It defines:

            :attributes: None.
            :methods:
                | test_arg_parser_success - Tests successful CLI argument parsing.
                | test_cli_bundle_validation - Tests validation checks of CLIBundle.
                | test_cli_run_executes_command - Tests that CLI.run executes matching command strategy.
                | test_gen_config_command_metadata - Tests GenConfigCommand properties.
                | test_gen_service_command_metadata - Tests GenServiceCommand properties.
                | test_cli_bundle_helpers - Tests CLIBundle helper methods.
                | test_cli_run_failure_with_unexpected_exception - Tests that CLI.run prints error and does not execute if unexpected exception.
                | test_cli_bundle_validate_commands_none - Tests CLIBundle validation with None commands.
                | test_cli_init_missing_bundle - Tests CLI init with None bundle.
                | test_init_failure_with_unexpected_exception - Tests engine behavior when dependency initialization fails with unexpected exception.
                | test_concrete_file_writer_read_failure - Tests file writing failure when underlying file system operation raises exception.
                | test_file_reader_not_found - Tests file reading with non-existing file.
                | test_concrete_template_provider - Tests concrete TemplateProvider.
                | test_concrete_subprocessor - Tests concrete SubProcessor.
                | test_subprocessor_execution_error - Tests SubProcessor execution error handling.
    '''

    def test_arg_parser_success(self) -> None:
        '''
            Tests successful registration and parsing of CLI arguments.

            :exceptions: None.
        '''
        context: ContextBundle = ContextBundle(checker=Checker(), reporter=Reporter(), verbose=False)
        params: dict[str, str] = {
            'ats_name': 'test_cli',
            'ats_version': '1.0.5',
            'ats_licence': 'MIT',
            'ats_build_date': '2026-06-22'
        }
        bundle: OptionComponentBundle = OptionComponentBundle(parameters=params, context_bundle=context)
        parser: OptionManager = OptionManager(bundle)

        cmd: DummyCommand = DummyCommand()
        parser.register_commands([cmd])

        test_args: list[str] = ["main.py", "dummy", "--req", "val", "--foo", "baz"]
        cmd_name: str
        params: dict[str, str]

        with patch("sys.argv", test_args):
            cmd_name, params = parser.parse_command()

        self.assertEqual(cmd_name, "dummy")
        self.assertEqual(params["req"], "val")
        self.assertEqual(params["foo"], "baz")

    def test_cli_bundle_validation(self) -> None:
        '''
            Tests validation checks of CLIBundle.

            :exceptions: None.
        '''
        bundle: CLIBundle = CLIBundle(service=None, parser=None, commands=None)
        with self.assertRaises(ValueError):
            bundle.validate()

        bundle_partial: CLIBundle = CLIBundle(service=MagicMock(), parser=None, commands=[])
        with self.assertRaises(ValueError):
            bundle_partial.validate()

    def test_cli_run_executes_command(self) -> None:
        '''
            Tests that CLI.run parses arguments and delegates execution to the matched command.

            :exceptions: None.
        '''
        mock_service: MagicMock = MagicMock(spec=IService)
        mock_parser: MagicMock = MagicMock(spec=IOptionManager)
        mock_command: MagicMock = MagicMock(spec=ICLICommand)
        mock_command.name = "dummy"

        mock_parser.parse_command.return_value = ("dummy", {"foo": "bar"})

        cli_bundle: CLIBundle = CLIBundle(service=mock_service, parser=mock_parser, commands=[mock_command])
        cli: CLI = CLI(cli_bundle)
        cli.run()

        mock_parser.parse_command.assert_called_once()
        mock_command.execute.assert_called_once_with({"foo": "bar"}, mock_service)

        self.assertIsNotNone(str(cli))
        self.assertIsNotNone(repr(cli))
        self.assertIsInstance(str(cli), str)
        self.assertIsInstance(repr(cli), str)
        self.assertNotEqual(str(cli), "")
        self.assertNotEqual(repr(cli), "")



    def test_cli_bundle_helpers(self) -> None:
        '''
            Tests CLIBundle helper methods (merge, to_dict).

            :exceptions: None.
        '''
        mock_service: MagicMock = MagicMock(spec=IService)
        mock_parser: MagicMock = MagicMock(spec=IOptionManager)

        bundle1: CLIBundle = CLIBundle(service=mock_service, parser=None, commands=None)
        bundle2: CLIBundle = CLIBundle(service=None, parser=mock_parser, commands=[])
        bundle1.merge(bundle2)

        self.assertEqual(bundle1.service, mock_service)
        self.assertEqual(bundle1.parser, mock_parser)
        self.assertEqual(bundle1.commands, [])

        d: dict[str, Any] = bundle1.to_dict()
        self.assertEqual(d["service"], mock_service)
        self.assertEqual(d["parser"], mock_parser)
        self.assertEqual(d["commands"], [])

    def test_cli_bundle_validate_commands_none(self) -> None:
        '''
            Tests CLIBundle validate raises ValueError when commands list is None.

            :exceptions: None.
        '''
        bundle: CLIBundle = CLIBundle(service=MagicMock(), parser=MagicMock(), commands=None)
        with self.assertRaises(ValueError):
            bundle.validate()

    def test_cli_init_missing_bundle(self) -> None:
        '''
            Tests CLI initialization raises ValueError when bundle is None.

            :exceptions: None.
        '''
        with self.assertRaises(ValueError):
            CLI(None)

    def test_command_option_init(self) -> None:
        '''
            Tests CommandOption initialization and attributes.

            :exceptions: None.
        '''
        opt: CommandOption = CommandOption(
            name="--test",
            help_text="Test description",
            default="default_val",
            required=True,
            choices=["choice1", "choice2"]
        )
        self.assertEqual(opt.name, "--test")
        self.assertEqual(opt.help_text, "Test description")
        self.assertEqual(opt.default, "default_val")
        self.assertTrue(opt.required)
        self.assertEqual(opt.choices, ["choice1", "choice2"])




class TestDNSResolver(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = DNSResolver()

    def test_resolver_str(self) -> None:
        self.assertIsNotNone(str(self.resolver))

    def test_resolver_is_initialized(self) -> None:
        self.assertTrue(self.resolver.is_initialized())

    def test_resolve_invalid_params(self) -> None:
        with self.assertRaises(TypeError):
            self.resolver.resolve(123)
        with self.assertRaises(ValueError):
            self.resolver.resolve("")

    def test_reverse_resolve_invalid_params(self) -> None:
        with self.assertRaises(TypeError):
            self.resolver.reverse_resolve(123)
        with self.assertRaises(ValueError):
            self.resolver.reverse_resolve("")

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_success(self, mock_resolve: MagicMock) -> None:
        mock_rrset = MagicMock()
        mock_rrset.__str__.return_value = "google.com. 300 IN A 1.2.3.4"
        mock_result = MagicMock()
        mock_result.rrset = mock_rrset
        mock_resolve.return_value = mock_result

        res = self.resolver.resolve("google.com")
        self.assertEqual(res, "1.2.3.4")

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_not_found(self, mock_resolve: MagicMock) -> None:
        from dns.resolver import NXDOMAIN
        mock_resolve.side_effect = NXDOMAIN()
        res = self.resolver.resolve("nonexistent.com")
        self.assertIsNone(res)

    @patch('socket.gethostbyaddr')
    def test_reverse_resolve_success(self, mock_gethostbyaddr: MagicMock) -> None:
        mock_gethostbyaddr.return_value = ("host.domain.com", [], ["1.2.3.4"])
        res = self.resolver.reverse_resolve("1.2.3.4")
        self.assertEqual(res, ["host.domain.com"])

    @patch('socket.gethostbyaddr')
    def test_reverse_resolve_failure(self, mock_gethostbyaddr: MagicMock) -> None:
        import socket
        mock_gethostbyaddr.side_effect = socket.herror()
        res = self.resolver.reverse_resolve("1.2.3.4")
        self.assertIsNone(res)


class TestExploreCommand(unittest.TestCase):
    def setUp(self) -> None:
        context = ContextBundle(checker=Checker(), reporter=Reporter(), verbose=False)
        self.command = ExploreCommand(context)

    def test_init_missing_bundle(self) -> None:
        from ats_utilities.exceptions.ats_value_error import ATSValueError
        with self.assertRaises(ATSValueError):
            ExploreCommand(None)

    def test_command_metadata(self) -> None:
        self.assertEqual(self.command.name, "explore")
        self.assertIsNotNone(self.command.help_text)
        self.assertEqual(len(self.command.options), 3)
        self.assertIsNotNone(str(self.command))

    def test_execute(self) -> None:
        service = MagicMock(spec=IService)
        service.explore.return_value = [
            ResolvedDomain(
                domain="www.google.com",
                ip="1.2.3.4",
                reverse=["host.google.com"]
            )
        ]

        res = self.command.execute({"domain": "google.com", "cluster": 2, "verbose": "True"}, service)
        self.assertEqual(res["returncode"], 0)
        self.assertEqual(res["stdout"], "explore done")

        service.explore.assert_called_once_with(domain="google.com", cluster=2, verbose=True)


class TestRecordsCommand(unittest.TestCase):
    def setUp(self) -> None:
        context = ContextBundle(checker=Checker(), reporter=Reporter(), verbose=False)
        self.command = RecordsCommand(context)

    def test_init_missing_bundle(self) -> None:
        from ats_utilities.exceptions.ats_value_error import ATSValueError
        with self.assertRaises(ATSValueError):
            RecordsCommand(None)

    def test_command_metadata(self) -> None:
        self.assertEqual(self.command.name, "records")
        self.assertIsNotNone(self.command.help_text)
        self.assertEqual(len(self.command.options), 1)
        self.assertIsNotNone(str(self.command))

    def test_execute(self) -> None:
        service = MagicMock(spec=IService)
        service.get_records.return_value = [
            DNSRecord(
                record_type="A",
                value="1.2.3.4"
            )
        ]

        res = self.command.execute({"domain": "google.com"}, service)
        self.assertEqual(res["returncode"], 0)
        self.assertEqual(res["stdout"], "records done")

        service.get_records.assert_called_once_with(domain="google.com")


# Extend TestDNSResolver with resolve_record tests
class TestDNSResolverExtended(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = DNSResolver()

    def test_resolve_record_invalid_params(self) -> None:
        with self.assertRaises(TypeError):
            self.resolver.resolve_record(123, "A")
        with self.assertRaises(ValueError):
            self.resolver.resolve_record("", "A")
        with self.assertRaises(TypeError):
            self.resolver.resolve_record("google.com", 123)
        with self.assertRaises(ValueError):
            self.resolver.resolve_record("google.com", "")

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_record_success(self, mock_resolve: MagicMock) -> None:
        mock_rrset = [MagicMock()]
        mock_rrset[0].__str__.return_value = "1.2.3.4"
        mock_resolve.return_value = mock_rrset

        res = self.resolver.resolve_record("google.com", "A")
        self.assertEqual(res, ["1.2.3.4"])

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_record_failure(self, mock_resolve: MagicMock) -> None:
        from dns.resolver import NXDOMAIN
        mock_resolve.side_effect = NXDOMAIN()
        res = self.resolver.resolve_record("nonexistent.com", "MX")
        self.assertEqual(res, [])

    @patch('dns_explorer.infrastructure.dns_resolver.resolve')
    def test_resolve_record_unexpected_exception(self, mock_resolve: MagicMock) -> None:
        mock_resolve.side_effect = RuntimeError("unexpected error")
        res = self.resolver.resolve_record("google.com", "A")
        self.assertEqual(res, [])


class TestResolveCommand(unittest.TestCase):
    def setUp(self) -> None:
        context = ContextBundle(checker=Checker(), reporter=Reporter(), verbose=False)
        self.command = ResolveCommand(context)

    def test_init_missing_bundle(self) -> None:
        from ats_utilities.exceptions.ats_value_error import ATSValueError
        with self.assertRaises(ATSValueError):
            ResolveCommand(None)

    def test_command_metadata(self) -> None:
        self.assertEqual(self.command.name, "resolve")
        self.assertIsNotNone(self.command.help_text)
        self.assertEqual(len(self.command.options), 2)
        self.assertIsNotNone(str(self.command))

    def test_execute_success(self) -> None:
        service = MagicMock(spec=IService)
        service.check_dns.return_value = ResolvedDomain(
            domain="google.com",
            ip="1.2.3.4",
            reverse=["host.google.com"]
        )

        res = self.command.execute({"domain": "google.com", "verbose": "True"}, service)
        self.assertEqual(res["returncode"], 0)
        self.assertEqual(res["stdout"], "resolved google.com")

        service.check_dns.assert_called_once_with(domain="google.com", verbose=True)

    def test_execute_failure(self) -> None:
        service = MagicMock(spec=IService)
        service.check_dns.return_value = None

        res = self.command.execute({"domain": "google.com", "verbose": "False"}, service)
        self.assertEqual(res["returncode"], 1)
        self.assertEqual(res["stderr"], "resolution failed for google.com")

        service.check_dns.assert_called_once_with(domain="google.com", verbose=False)


class TestReverseCommand(unittest.TestCase):
    def setUp(self) -> None:
        context = ContextBundle(checker=Checker(), reporter=Reporter(), verbose=False)
        self.command = ReverseCommand(context)

    def test_init_missing_bundle(self) -> None:
        from ats_utilities.exceptions.ats_value_error import ATSValueError
        with self.assertRaises(ATSValueError):
            ReverseCommand(None)

    def test_command_metadata(self) -> None:
        self.assertEqual(self.command.name, "reverse")
        self.assertIsNotNone(self.command.help_text)
        self.assertEqual(len(self.command.options), 1)
        self.assertIsNotNone(str(self.command))

    def test_execute_success(self) -> None:
        service = MagicMock(spec=IService)
        service.reverse_resolve.return_value = ["host.google.com"]

        res = self.command.execute({"ip": "8.8.8.8"}, service)
        self.assertEqual(res["returncode"], 0)
        self.assertEqual(res["stdout"], "reverse resolved 8.8.8.8")

        service.reverse_resolve.assert_called_once_with(ip="8.8.8.8")

    def test_execute_failure(self) -> None:
        service = MagicMock(spec=IService)
        service.reverse_resolve.return_value = []

        res = self.command.execute({"ip": "8.8.8.8"}, service)
        self.assertEqual(res["returncode"], 1)
        self.assertEqual(res["stderr"], "no hostnames found for 8.8.8.8")

        service.reverse_resolve.assert_called_once_with(ip="8.8.8.8")






