# -*- coding: UTF-8 -*-

'''
Module
    validator.py
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
    A validator for the dns_explorer bundle.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_value import not_none
from ats_utilities.validation.check_type import istype

from dns_explorer.setup.bundle import DNSExplorerBundle
from dns_explorer.core.service.iservice import IService
from dns_explorer.core.service.idns_resolver import IDNSResolver
from dns_explorer.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DNSExplorerBundleValidator:
    '''
        A validator for the dns_explorer bundle.

        It defines:

            :methods:
                | validate - Validates the dns_explorer bundle.
                | is_valid - Checks if the dns_explorer bundle is valid.
    '''

    @classmethod
    def validate(cls, bundle: DNSExplorerBundle) -> None:
        '''
            Validates the dns_explorer bundle.

            :param bundle: The dns_explorer bundle to be validated.
            :exceptions:
                | ATSValueError: The dns_explorer bundle must be provided and have proper values.
                | ATSTypeError:  The dns_explorer bundle must be an instance of DNSExplorerBundle and
                |                its attributes must be instances of their respective types.
        '''
        ctx: str = 'dns_explorer_bundle_validator::validate(...)'
        msg_bundle_none: str = 'the dns_explorer bundle must be provided'
        msg_bundle_istype: str = 'the dns_explorer bundle must be an instance of DNSExplorerBundle'
        msg_base_none: str = 'the base bundle must be provided'
        msg_service_none: str = 'the service must be provided'
        msg_dns_resolver_none: str = 'the dns_resolver must be provided'
        msg_cli_none: str = 'the cli must be provided'
        msg_base_istype: str = 'the base bundle must be an instance of BaseBundle'
        msg_service_istype: str = 'the service must be an instance of IService'
        msg_dns_resolver_istype: str = 'the dns_resolver must be an instance of IDNSResolver'
        msg_cli_istype: str = 'the cli must be an instance of ICLI'

        not_none(bundle, ctx, msg_bundle_none)
        istype(bundle, DNSExplorerBundle, ctx, msg_bundle_istype)

        not_none(bundle.base, ctx, msg_base_none)
        not_none(bundle.service, ctx, msg_service_none)
        not_none(bundle.dns_resolver, ctx, msg_dns_resolver_none)
        not_none(bundle.cli, ctx, msg_cli_none)

        istype(bundle.base, BaseBundle, ctx, msg_base_istype)
        istype(bundle.service, IService, ctx, msg_service_istype)
        istype(bundle.dns_resolver, IDNSResolver, ctx, msg_dns_resolver_istype)
        istype(bundle.cli, ICLI, ctx, msg_cli_istype)

    @classmethod
    def is_valid(cls, bundle: DNSExplorerBundle) -> bool:
        '''
            Checks if the dns_explorer bundle is valid.

            :param bundle: The dns_explorer bundle to be checked.
            :return: True if valid, False otherwise.
        '''
        try:
            cls.validate(bundle)
            return True

        except (ATSValueError, ATSTypeError):
            return False
