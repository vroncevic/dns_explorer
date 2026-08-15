# -*- coding: UTF-8 -*-

'''
Module
    reverse_command_executor.py
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
    Defines ReverseCommandExecutor class.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.checker.ichecker import IChecker
from ats_utilities.reporter.ireporter import IReporter
from ats_utilities.exceptions import ATSValueError
from ats_utilities.utils.reflection import to_str

from dns_explorer.infrastructure.command.icommand_definition import ICommandDefinition
from dns_explorer.core.service.iservice import IService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReverseCommandExecutor:
    '''
        Command executor strategy for reverse DNS query.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
                | _checker - Injected parameters checker.
                | _reporter - Injected reporter for messaging.
                | _verbose - Injected Enable/Disable verbose option.
            :methods:
                | execute - Executes the subcommand.
                | get_definition - Returns the command definition metadata.
                | __str__ - Returns the ReverseCommandExecutor as string representation.
    '''

    definition: ICommandDefinition
    _checker: IChecker
    _reporter: IReporter
    _verbose: bool

    def __init__(self, definition: ICommandDefinition, bundle: ContextBundle) -> None:
        '''
            Initializes ReverseCommandExecutor.

            :param definition: The command definition metadata.
            :param bundle: Context bundle to use for command execution.
            :exceptions:
                | ATSValueError: If the context bundle is not provided.
        '''
        if not bundle:
            raise ATSValueError('context bundle must be provided.')

        self.definition = definition
        self._checker = bundle.checker
        self._reporter = bundle.reporter
        self._verbose = bundle.verbose

    def execute(self, *, params: Mapping[str, object], service: IService) -> Mapping[str, object]:
        '''
            Executes the subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: Command orchestrator service instance.
            :return: Mapping containing the return code, stdout, and stderr.
        '''
        ip: str = str(params.get("ip", ""))
        self._reporter.success([f"\n    dns_explorer::pro::dns_processor Querying reverse DNS for {ip}\n"])
        hostnames: list[str] = service.reverse_resolve(ip=ip)

        if hostnames:
            self._reporter.success([f"\n    Reverse hostnames for {ip}:"])

            for host in hostnames:
                self._reporter.success([f"        - {host}"])

            self._reporter.success([""])

            return {"returncode": 0, "stdout": f"reverse resolved {ip}", "stderr": ""}
        else:
            self._reporter.success([f"\nNo reverse hostnames found for {ip}\n"])

            return {"returncode": 1, "stdout": "", "stderr": f"no hostnames found for {ip}"}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
        '''
        return self.definition

    def __str__(self) -> str:
        '''
            Returns the ReverseCommandExecutor as string representation.

            :return: The ReverseCommandExecutor as string representation.
        '''
        return to_str(self)
