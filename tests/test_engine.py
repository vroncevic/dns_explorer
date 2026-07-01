# -*- coding: UTF-8 -*-

'''
Module
    test_engine.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    dns_explorer is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 30 of the License, or
    (at your option) any later version.
    dns_explorer is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for main engine (DNSExplorer).
'''

import unittest
from unittest.mock import MagicMock, patch
from dns_explorer.engine import DNSExplorer
from dns_explorer.dns_explorer_bundle import DNSExplorerBundle
from dns_explorer.domain.ports.iservice import IService
from dns_explorer.domain.ports.idns_resolver import IDNSResolver
from ats_utilities.option.ioption_parser import IOptionManager
from ats_utilities.exceptions.ats_value_error import ATSValueError
from dns_explorer.infrastructure.icli import ICLI

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class TestEngine(unittest.TestCase):
    '''
        Defines engine unit tests.

        It defines:

            :attributes: None
            :methods:
                | test_default_init - Tests default constructor initialization.
                | test_custom_injection - Tests custom dependency injection in DNSExplorer.
                | test_init_failure - Tests engine behavior when dependency initialization fails.
                | test_dns_explorer_bundle_helpers - Tests DNSExplorerBundle helpers.
                | test_init_failure_with_unexpected_exception - Tests engine behavior when dependency initialization fails with unexpected exception.
                | test_process_success - Tests that process() executes CLI if initialized.
                | test_process_failure - Tests that process() prints error and does not execute if uninitialized.
                | test_process_failure_with_unexpected_exception - Tests that process() prints error and does not execute if unexpected exception.
    '''

    def test_default_init(self) -> None:
        '''
            Tests default constructor initialization of DNSExplorer.

            :exceptions: None.
        '''
        engine: DNSExplorer = DNSExplorer()
        self.assertTrue(engine._is_initialized)
        self.assertIsNotNone(engine._cli)

    def test_custom_injection(self) -> None:
        '''
            Tests custom dependency injection in DNSExplorer constructor.

            :exceptions: None.
        '''
        mock_service: MagicMock = MagicMock(spec=IService)
        mock_parser: MagicMock = MagicMock(spec=IOptionManager)
        mock_cli: MagicMock = MagicMock(spec=ICLI)
        mock_resolver: MagicMock = MagicMock(spec=IDNSResolver)

        bundle: DNSExplorerBundle = DNSExplorerBundle(
            service=mock_service,
            parser=mock_parser,
            cli=mock_cli,
            dns_resolver=mock_resolver
        )

        engine: DNSExplorer = DNSExplorer(bundle)
        self.assertTrue(engine._is_initialized)
        self.assertEqual(engine._cli, mock_cli)

    def test_not_initialized_engine(self) -> None:
        '''
            Tests not initialized engine.

            :exceptions: None.
        '''
        with patch.object(DNSExplorer, "_info_file", "invalid/path/dns_explorer.cfg"):
            engine: DNSExplorer = DNSExplorer()
            self.assertFalse(engine._is_initialized)

    def test_init_failure(self) -> None:
        '''
            Tests engine behavior when dependency initialization fails.

            :exceptions: None.
        '''
        error_message: str = "Service initialization failed"

        with patch('dns_explorer.engine.Service', side_effect=ATSValueError(error_message)):
            with patch('builtins.print') as mock_print:
                engine: DNSExplorer = DNSExplorer()
                self.assertFalse(engine._is_initialized)
                mock_print.assert_called_with(f'\x1b[31m❌ dns_explorer: {error_message}\x1b[0m')

    def test_process_failure_with_unexpected_exception(self) -> None:
        '''
            Tests that process() prints error and does not execute if unexpected exception.

            :exceptions: None.
        '''
        with patch('dns_explorer.engine.Service', side_effect=RuntimeError("unexpected error.")):
            with patch('builtins.print') as mock_print:
                engine: DNSExplorer = DNSExplorer()
                engine.process()
                mock_print.assert_any_call(f'\x1b[31m❌ dns_explorer unexpected exception: unexpected error.\x1b[0m')

    def test_process_success(self) -> None:
        '''
            Tests that process() executes CLI if initialized.

            :exceptions: None.
        '''
        mock_cli: MagicMock = MagicMock(spec=ICLI)
        mock_cli.run.return_value = {"returncode": 0, "stdout": "success", "stderr": ""}
        mock_resolver: MagicMock = MagicMock(spec=IDNSResolver)
        bundle: DNSExplorerBundle = DNSExplorerBundle(cli=mock_cli, dns_resolver=mock_resolver)

        engine: DNSExplorer = DNSExplorer(bundle)
        self.assertTrue(engine._is_initialized)

        engine.process()
        mock_cli.run.assert_called_once()

    def test_process_failure_exit_code(self) -> None:
        '''
            Tests that process() handles non-zero returncode from CLI.

            :exceptions: None.
        '''
        mock_cli: MagicMock = MagicMock(spec=ICLI)
        mock_cli.run.return_value = {"returncode": 1, "stdout": "", "stderr": "Command failed"}
        mock_resolver: MagicMock = MagicMock(spec=IDNSResolver)
        bundle: DNSExplorerBundle = DNSExplorerBundle(cli=mock_cli, dns_resolver=mock_resolver)

        engine: DNSExplorer = DNSExplorer(bundle)
        self.assertTrue(engine._is_initialized)

        engine.process()
        mock_cli.run.assert_called_once()

    def test_process_failure(self) -> None:
        '''
            Tests that process() prints error and does not execute if uninitialized.

            :exceptions: None.
        '''
        with patch('dns_explorer.engine.Service', side_effect=ATSValueError("Service initialization failed")):
            with patch('builtins.print') as mock_print:
                engine: DNSExplorer = DNSExplorer()
                self.assertFalse(engine._is_initialized)

                engine.process()
                mock_print.assert_any_call('\x1b[31m❌ dns_explorer: engine not initialized.\x1b[0m')

    def test_dns_explorer_bundle_helpers(self) -> None:
        '''
            Tests DNSExplorerBundle merge and to_dict helpers.

            :exceptions: None.
        '''
        resolver1: MagicMock = MagicMock(spec=IDNSResolver)
        service1: MagicMock = MagicMock(spec=IService)
        parser1: MagicMock = MagicMock(spec=IOptionManager)
        cli1: MagicMock = MagicMock(spec=ICLI)

        bundle1: DNSExplorerBundle = DNSExplorerBundle(dns_resolver=resolver1, service=None)
        bundle2: DNSExplorerBundle = DNSExplorerBundle(dns_resolver=None, service=service1)
        bundle1.merge(bundle2)

        self.assertEqual(bundle1.dns_resolver, resolver1)
        self.assertEqual(bundle1.service, service1)

        d = bundle1.to_dict()
        self.assertEqual(d["dns_resolver"], resolver1)
        self.assertEqual(d["service"], service1)

        bundle3: DNSExplorerBundle = DNSExplorerBundle(
            service=service1, parser=parser1, cli=cli1, dns_resolver=None
        )
        with self.assertRaises(ATSValueError):
            bundle3.validate()

        bundle4: DNSExplorerBundle = DNSExplorerBundle(
            service=None, parser=parser1, cli=cli1, dns_resolver=resolver1
        )
        with self.assertRaises(ATSValueError):
            bundle4.validate()

        bundle5: DNSExplorerBundle = DNSExplorerBundle(
            service=service1, parser=None, cli=cli1, dns_resolver=resolver1
        )
        with self.assertRaises(ATSValueError):
            bundle5.validate()

        bundle6: DNSExplorerBundle = DNSExplorerBundle(
            service=service1, parser=parser1, cli=None, dns_resolver=resolver1
        )
        with self.assertRaises(ATSValueError):
            bundle6.validate()

        bundle_ok: DNSExplorerBundle = DNSExplorerBundle(
            service=service1, parser=parser1, cli=cli1, dns_resolver=resolver1
        )
        bundle_ok.validate()
