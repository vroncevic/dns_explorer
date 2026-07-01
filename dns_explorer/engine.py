# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Main engine orchestrator class for Task Code Generator CLI.
'''

from typing import Any, override
from os.path import dirname, realpath
from ats_utilities.base.engine import Base
from ats_utilities.base.component_bundle import BaseComponentBundle
from ats_utilities.option.ioption_parser import IOptionManager
from ats_utilities.exceptions.ats_value_error import ATSValueError
from dns_explorer.dns_explorer_bundle import DNSExplorerBundle
from dns_explorer.domain.ports.iservice import IService
from dns_explorer.application.service import Service
from dns_explorer.domain.ports.idns_resolver import IDNSResolver
from dns_explorer.infrastructure.dns_resolver import DNSResolver
from dns_explorer.infrastructure.explore_command import ExploreCommand
from dns_explorer.infrastructure.records_command import RecordsCommand
from dns_explorer.infrastructure.resolve_command import ResolveCommand
from dns_explorer.infrastructure.reverse_command import ReverseCommand
from dns_explorer.infrastructure.icli_command import ICLICommand
from dns_explorer.infrastructure.cli_bundle import CLIBundle
from dns_explorer.infrastructure.icli import ICLI
from dns_explorer.infrastructure.cli import CLI

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class DNSExplorer(Base):
    '''
        Engine orchestrating the initialization and execution of DNSExplorer.

        It defines:

            :attributes:
                | _info_file - Path to the info file.
                | _cli - Adapter for command line user interface.
            :methods:
                | __init__ - Initializes the DNSExplorer engine with adapters and services.
                | run - Starts the dns_explorer.
    '''

    _info_file: str = 'infrastructure/config/dns_explorer.cfg'

    def __init__(self, component_bundle: DNSExplorerBundle | None = None) -> None:
        '''
            Initializes the DNSExplorer engine with adapters and services.

            :param component_bundle: DNSExplorer bundle containing adapters and services | None.
            :type component_bundle: <DNSExplorerBundle | None>
            :exceptions: None.
        '''
        current_dir: str = dirname(realpath(__file__))
        super().__init__(BaseComponentBundle(info_file=f'{current_dir}/{self._info_file}'))

        try:
            if not self._is_initialized:
                raise ATSValueError(f'failed to initialize base engine with info file {current_dir}/{self._info_file}')

            # Mark as not initialized (waiting for other components to be initialized)
            self._is_initialized = False

            # Dependency injection: Dependency Inversion Principle
            # Use provided component bundle or use default adapters
            bundle: DNSExplorerBundle = component_bundle or DNSExplorerBundle()

            # Initialization of option manager adapter (Adapter for options parsing)
            parser: IOptionManager = bundle.parser or self._options_parser

            # Initialize dns resolver adapter
            dns_resolver: IDNSResolver = bundle.dns_resolver or DNSResolver()

            # Injecting adapter into the application service (Orchestration)
            # Force default implementation of service if not provided by bundle
            service: IService = bundle.service or Service(dns_resolver=dns_resolver)

            # Setting up CLI command strategies
            commands: list[ICLICommand] = [
                ExploreCommand(self.get_shared_context()),
                RecordsCommand(self.get_shared_context()),
                ResolveCommand(self.get_shared_context()),
                ReverseCommand(self.get_shared_context())
            ]

            # Setting up primary adapter (CLI interface)
            cli_bundle: CLIBundle = CLIBundle(service=service, parser=parser, commands=commands)
            self._cli: ICLI = bundle.cli or CLI(cli_bundle)

            # Mark as initialized (all components initialized)
            self._is_initialized = all([
               component.is_initialized() for component in [parser, service, dns_resolver, self._cli] if component
            ])
            self._reporter.success(['✅ dns_explorer: engine initialized successfully.'])

        except ATSValueError as exc:
            self._reporter.error([f'❌ dns_explorer: {exc}'])
        except Exception as exc:
            self._reporter.error([f'❌ dns_explorer unexpected exception: {exc}'])

    @override
    def process(self) -> None:
        '''
            Runs the dns_explorer.

            :exceptions: None.
        '''
        result: dict[str, Any] = {}

        if self.is_initialized():
            self._reporter.success(['🔥 Starting execution command...'])
            result = self._cli.run()
            self._reporter.success(['✅ Execution finished!'])

            if result.get("returncode") != 0:
                self._reporter.error([f'❌ dns_explorer: {result.get("stderr") or "failed!"}'])
                self._reporter.error(['❌ dns_explorer: exiting with error.'])
            else:
                self._reporter.success([f'✅ dns_explorer: {result.get("stdout") or "done!"}'])
                self._reporter.success(['✅ dns_explorer: exiting successfully.'])
        else:
            self._reporter.error(['❌ dns_explorer: engine not initialized.'])
