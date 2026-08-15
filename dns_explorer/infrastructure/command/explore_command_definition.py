# -*- coding: UTF-8 -*-

'''
Module
    explore_command_definition.py
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
    Defines ExploreCommandDefinition class.
'''

from __future__ import annotations

from collections.abc import Sequence

from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExploreCommandDefinition:
    '''
        CLI subcommand metadata definition for DNS exploration.

        It defines:

            :methods:
                | name - Returns the command name.
                | help_text - Returns the command help text.
                | options - Returns the sequence of command options.
                | __str__ - Returns the command definition as string representation.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the command name.

            :return: The command name.
        '''
        return 'explore'

    @property
    def help_text(self) -> str:
        '''
            Returns the command help text.

            :return: The command help text.
        '''
        return 'DNS exploration command'

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns the command options.

            :return: Sequence of command options.
        '''
        return [
            OptionData(
                name="--domain",
                help_text="Domain name to scan",
                action=None,
                default=None,
                required=True,
                choices=None,
                nargs=None
            ),
            OptionData(
                name="--cluster",
                help_text="Count of cluster subdomains to scan",
                action=None,
                default="0",
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name="--verbose",
                help_text="Activate verbose mode (True/False)",
                action=None,
                default="False",
                required=False,
                choices=["True", "False"],
                nargs=None
            )
        ]

    def __str__(self) -> str:
        '''
            Returns the command definition as string representation.

            :return: The command definition as string representation.
        '''
        return to_str(self)
