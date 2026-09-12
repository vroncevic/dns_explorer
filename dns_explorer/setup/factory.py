# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory for creating the dns_explorer bundle.
'''

from __future__ import annotations

from os.path import abspath, dirname, join

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from dns_explorer.setup.bundle import DNSExplorerBundle
from dns_explorer.setup.options import DNSExplorerBundleOptions
from dns_explorer.setup.registry import DNSExplorerBundleRegistry
from dns_explorer.setup.dependencies import DNSExplorerBundleDependencies
from dns_explorer.setup.opt_validator import DNSExplorerBundleOptionsValidator
from dns_explorer.setup.keys import DNSExplorerBundleKeys

from dns_explorer.core.service.engine import Service
from dns_explorer.infrastructure.dns_resolver import DNSResolver
from dns_explorer.infrastructure.cli.engine import CLI
from dns_explorer.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from dns_explorer.infrastructure.cli.setup.registry import CLIBundleRegistry

from dns_explorer.infrastructure.command.command import CommandBundle
from dns_explorer.infrastructure.command.explore_command_definition import ExploreCommandDefinition
from dns_explorer.infrastructure.command.explore_command_executor import ExploreCommandExecutor
from dns_explorer.infrastructure.command.records_command_definition import RecordsCommandDefinition
from dns_explorer.infrastructure.command.records_command_executor import RecordsCommandExecutor
from dns_explorer.infrastructure.command.resolve_command_definition import ResolveCommandDefinition
from dns_explorer.infrastructure.command.resolve_command_executor import ResolveCommandExecutor
from dns_explorer.infrastructure.command.reverse_command_definition import ReverseCommandDefinition
from dns_explorer.infrastructure.command.reverse_command_executor import ReverseCommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DNSExplorerBundleFactory:
    '''
        Factory for creating the dns_explorer bundle.

        It defines:

            :attributes:
                | _info_file - Path to the dns_explorer info file.
            :methods:
                | create_bundle - Creates the dns_explorer bundle with optional pre-configured options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'dns_explorer.cfg'
    )

    @classmethod
    def create_bundle(cls, options: DNSExplorerBundleOptions | None = None) -> DNSExplorerBundle:
        '''
            Creates the dns_explorer bundle with optional pre-configured options.

            :param options: The pre-configured options for the dns_explorer bundle.
            :return: The dns_explorer bundle.
            :exceptions:
                | ATSValueError: The dns_explorer bundle options must be provided and have proper values.
                | ATSTypeError:  The dns_explorer bundle options must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The dns_explorer bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The dns_explorer bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The dns_explorer bundle must be provided and have proper values.
                | ATSTypeError:  The dns_explorer bundle must be an instance of DNSExplorerBundle and
                |                its attributes must be instances of their respective types.
        '''
        if options is not None:
            DNSExplorerBundleOptionsValidator.validate(options)

        info_file = options.get(DNSExplorerBundleKeys.OPTION_INFO_FILE) if options else cls._info_file

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dns_resolver: DNSResolver = DNSResolver()

        service: Service = Service(dns_resolver=dns_resolver)

        explore_definition = ExploreCommandDefinition()
        explore_cmd = CommandBundle(
            definition=explore_definition,
            executor=ExploreCommandExecutor(explore_definition, context_bundle)
        )

        records_definition = RecordsCommandDefinition()
        records_cmd = CommandBundle(
            definition=records_definition,
            executor=RecordsCommandExecutor(records_definition, context_bundle)
        )

        resolve_definition = ResolveCommandDefinition()
        resolve_cmd = CommandBundle(
            definition=resolve_definition,
            executor=ResolveCommandExecutor(resolve_definition, context_bundle)
        )

        reverse_definition = ReverseCommandDefinition()
        reverse_cmd = CommandBundle(
            definition=reverse_definition,
            executor=ReverseCommandExecutor(reverse_definition, context_bundle)
        )

        cli_bundle = CLIBundleRegistry.create_bundle(
            dependencies=CLIBundleDependencies(
                service=service,
                parser=base_bundle.option_manager,
                commands=[explore_cmd, records_cmd, resolve_cmd, reverse_cmd]
            )
        )

        cli = CLI(cli_bundle)

        return DNSExplorerBundleRegistry.create_bundle(
            dependencies=DNSExplorerBundleDependencies(
                base=base_bundle,
                service=service,
                dns_resolver=dns_resolver,
                cli=cli
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version.

            :return: The factory version.
            :exceptions: None.
        '''
        return __version__
