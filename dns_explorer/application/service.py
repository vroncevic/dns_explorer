# -*- coding: UTF-8 -*-

'''
Module
    service.py
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
    Service for orchestrating the tool execution process.
'''

from typing import override
from dns_explorer.domain.ports.iservice import IService
from dns_explorer.domain.ports.idns_resolver import IDNSResolver
from dns_explorer.domain.models import ResolvedDomain, DNSRecord

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/dns_explorer'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__: str = '1.0.5'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Development'


class Service(IService):
    '''
        Service for orchestrating the tool execution process.

        It defines:

            :attributes:
                | _dns_resolver - Adapter for DNS resolution operations.
                | _SUBDOMAINS - List of _SUBDOMAINS to explore.
            :methods:
                | __init__ - Initializes the Service.
                | explore - Explores DNS _SUBDOMAINS.
                | check_dns - Executes dns request and reverse DNS lookup for a single domain.
                | get_records - Queries various DNS records for a domain.
                | reverse_resolve - Performs reverse DNS lookup on an IP address.
                | is_initialized - Checks if the service and its adapters are initialized.
    '''

    _SUBDOMAINS: list[str] = [
        'www', 'mail', 'remote', 'blog', 'webmail', 'server', 'ns', 'smtp',
        'pop', 'imap', 'admin', 'secure', 'vpn', 'dns', 'ftp', 'test',
        'portal', 'host', 'support', 'dev', 'web', 'mx', 'email', 'cloud',
        'owa', 'cdn', 'api', 'exchange', 'mysql', 'wiki', 'cpanel'
    ]

    def __init__(self, dns_resolver: IDNSResolver | None = None) -> None:
        '''
            Initializes the Service.

            :param dns_resolver: DNS resolver adapter.
            :type dns_resolver: <IDNSResolver | None>
            :exceptions:
                | ValueError: DNS resolver must be provided.
        '''
        if dns_resolver is None:
            raise ValueError("dns_resolver must be provided.")

        self._dns_resolver: IDNSResolver = dns_resolver

    @override
    def explore(self, domain: str, cluster: int, verbose: bool = False) -> list[ResolvedDomain]:
        '''
            Explores _SUBDOMAINS of a domain and resolves their DNS and reverse DNS.

            :param domain: Base domain name to explore.
            :type domain: <str>
            :param cluster: Number of _SUBDOMAINS in cluster to scan.
            :type cluster: <int>
            :param verbose: Enable/Disable verbose logging.
            :type verbose: <bool>
            :return: List of resolved domains.
            :rtype: <list[ResolvedDomain]>
            :exceptions:
                | ValueError: domain must be provided.
        '''
        if not domain:
            raise ValueError("domain must be provided.")

        results: list[ResolvedDomain] = []

        for sub_domain in self._SUBDOMAINS:
            sub_domain_final: str = f'{sub_domain}.{domain}'
            res = self.check_dns(sub_domain_final, verbose)

            if res:
                results.append(res)

            for i in range(0, cluster):
                sub_domain_multi: str = f'{sub_domain}{i}.{domain}'
                res = self.check_dns(sub_domain_multi, verbose)

                if res:
                    results.append(res)

        return results

    @override
    def check_dns(self, domain: str, verbose: bool = False) -> ResolvedDomain | None:
        '''
            Executes dns request and reverse DNS lookup.

            :param domain: Domain name to check.
            :type domain: <str>
            :param verbose: Enable/Disable verbose option.
            :type verbose: <bool>
            :return: ResolvedDomain instance or None.
            :rtype: <ResolvedDomain | None>
            :exceptions: None.
        '''
        try:
            ip_address: str | None = self._dns_resolver.resolve(domain)

            if ip_address:
                dns_reverse: list[str] | None = self._dns_resolver.reverse_resolve(ip_address)

                if dns_reverse:
                    return ResolvedDomain(
                        domain=domain,
                        ip=ip_address,
                        reverse=dns_reverse
                    )

        except Exception:
            pass

        return None

    @override
    def get_records(self, domain: str) -> list[DNSRecord]:
        '''
            Queries various DNS records for a domain.

            :param domain: Domain name.
            :type domain: <str>
            :return: List of DNS records.
            :rtype: <list[DNSRecord]>
            :exceptions:
                | ValueError: domain must be provided.
        '''
        if not domain:
            raise ValueError("domain must be provided.")

        record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA"]
        records: list[DNSRecord] = []

        for r_type in record_types:

            try:
                values = self._dns_resolver.resolve_record(domain, r_type)

                for val in values:
                    records.append(DNSRecord(record_type=r_type, value=val))

            except Exception:
                pass

        return records

    @override
    def reverse_resolve(self, ip: str) -> list[str]:
        '''
            Performs reverse DNS lookup on an IP address.

            :param ip: IP address.
            :type ip: <str>
            :return: List of resolved hostnames.
            :rtype: <list[str]>
            :exceptions:
                | ValueError: ip must be provided.
        '''
        if not ip:
            raise ValueError("ip must be provided.")

        try:

            res = self._dns_resolver.reverse_resolve(ip)

            return res if res else []

        except Exception:
            pass

        return []

    @override
    def is_initialized(self) -> bool:
        '''
            Checks if the service is initialized.

            :return: True if the service is initialized, False otherwise.
            :rtype: <bool>
            :exceptions: None.
        '''
        return all([self._dns_resolver is not None, self._dns_resolver.is_initialized()])

