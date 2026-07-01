# -*- coding: UTF-8 -*-

'''
Module
    records_command.py
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
    Defines RecordsCommand class implementing ICLICommand.
'''

from typing import Any, override
from ats_utilities.context_bundle import ContextBundle
from ats_utilities.checker.ichecker import IChecker
from ats_utilities.reporter.ireporter import IReporter
from ats_utilities.option.command_option import CommandOption
from ats_utilities.exceptions.ats_value_error import ATSValueError
from ats_utilities.factory_context_bundle import factory_context_bundle
from ats_utilities.factory_class import format_instance_to_string
from dns_explorer.domain.ports.iservice import IService
from dns_explorer.infrastructure.icli_command import ICLICommand
from dns_explorer.domain.models import DNSRecord

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class RecordsCommand(ICLICommand):
    '''
        Command strategy to query and display domain DNS records.

        It defines:

            :attributes:
                | _checker - Injected parameters checker (default Checker).
                | _reporter - Injected reporter for messaging (default Reporter).
                | _verbose - Injected Enable/Disable verbose option (default False).
            :methods:
                | name - Property returning name of the command.
                | help_text - Property returning help text of the command.
                | options - Property returning list of command options.
                | execute - Executes the subcommand actions.
                | __str__ - Returns the RecordsCommand as string representation.
    '''

    _checker: IChecker
    _reporter: IReporter
    _verbose: bool

    def __init__(self, bundle: ContextBundle) -> None:
        '''
            Initializes RecordsCommand.

            :param bundle: Context bundle to use for command execution.
            :type bundle: <ContextBundle>
            :exceptions:
                | ATSValueError: If the context bundle is not provided.
        '''
        if not bundle:
            raise ATSValueError('context bundle must be provided.')

        factory_context_bundle(self, bundle)

    @property
    @override
    def name(self) -> str:
        '''
            Returns command name.

            :return: The command name.
            :rtype: <str>
            :exceptions: None.
        '''
        return 'records'

    @property
    @override
    def help_text(self) -> str:
        '''
            Returns command help text.

            :return: The command help text.
            :rtype: <str>
            :exceptions: None.
        '''
        return 'Query various DNS records (A, AAAA, MX, TXT, NS, SOA) for a domain'

    @property
    @override
    def options(self) -> list[CommandOption]:
        '''
            Returns command options.

            :return: List of command options.
            :rtype: <List[CommandOption]>
            :exceptions: None.
        '''
        return [
            CommandOption(
                name="--domain",
                help_text="Domain name to query",
                required=True
            )
        ]

    @override
    def execute(self, params: dict[str, Any], service: IService) -> dict[str, Any]:
        '''
            Executes the subcommand.

            :param params: Subcommand parameters from CLI parser.
            :type params: <dict[str, Any]>
            :param service: Command orchestrator service instance.
            :type service: <IService>
            :return: <dict> containing the return code, stdout, and stderr of the command.
            :rtype: <dict[str, Any]>
            :exceptions: None.
        '''
        domain: str = params.get("domain", "")
        self._reporter.success([f"\n    dns_explorer::pro::dns_processor Querying DNS records for {domain}\n"])
        records: list[DNSRecord] = service.get_records(domain=domain)
        current_type: str = ""

        for rec in records:

            if rec.record_type != current_type:
                current_type = rec.record_type
                self._reporter.success([f"\n        --- {current_type} Records ---"])

            self._reporter.success([f"        {rec.value}"])

        self._reporter.success([""])

        return {"returncode": 0, "stdout": "records done", "stderr": ""}

    @override
    def __str__(self) -> str:
        '''
            Returns the RecordsCommand as string representation.

            :return: The RecordsCommand as string representation.
            :rtype: <str>
            :exceptions: None.
        '''
        return format_instance_to_string(self)
