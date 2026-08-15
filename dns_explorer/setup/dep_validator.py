# -*- coding: UTF-8 -*-

'''
Module
    dep_validator.py
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
    Validator for the dns_explorer bundle dependencies.
'''

from __future__ import annotations

from collections.abc import Mapping
from ats_utilities.exceptions import ATSValueError, ATSTypeError

from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from dns_explorer.setup.dependencies import DNSExplorerBundleDependencies
from dns_explorer.setup.keys import DNSExplorerBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DNSExplorerBundleDependenciesValidator:
    '''
        Validator for the dns_explorer bundle dependencies.

        It defines:

            :methods:
                | validate - Validates the dns_explorer bundle dependencies.
                | is_valid - Checks if the dns_explorer bundle dependencies is valid.
    '''

    @classmethod
    def validate(cls, dependencies: DNSExplorerBundleDependencies) -> None:
        '''
            Validates the dns_explorer bundle dependencies.

            :param dependencies: The dns_explorer bundle dependencies to be validated.
            :exceptions:
                | ATSValueError: The dns_explorer bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The dns_explorer bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
        '''
        ctx: str = 'dns_explorer_bundle_dependencies_validator::validate(...)'
        msg_dependencies_none: str = 'the dns_explorer bundle dependencies must be provided'
        msg_dependencies_istype: str = 'the dns_explorer bundle dependencies must be a Mapping'

        not_none(dependencies, ctx, msg_dependencies_none)
        istype(dependencies, Mapping, ctx, msg_dependencies_istype)

        for attr_name, expected_type in DNSExplorerBundleKeys.get_dependency_to_type().items():
            msg_attr_name_none: str = f'the {attr_name.replace("_", " ")} must be provided'
            msg_attr_name_istype: str = f'the {attr_name.replace("_", " ")} must be an instance of {expected_type.__name__}'

            attribute = dependencies.get(attr_name)

            not_none(attribute, ctx, msg_attr_name_none)
            istype(attribute, expected_type, ctx, msg_attr_name_istype)

    @classmethod
    def is_valid(cls, dependencies: DNSExplorerBundleDependencies) -> bool:
        '''
            Checks if the dns_explorer bundle dependencies is valid.

            :param dependencies: The dns_explorer bundle dependencies to be checked.
            :return: True if valid, False otherwise.
        '''
        try:
            cls.validate(dependencies)
            return True

        except (ATSValueError, ATSTypeError):
            return False
