from case_database import CaseDatabase
from host import Host
from ssl_certificate import SSLCertificate
from ssl_database import SSLDatabase


def get_hostnames():
    host_database = SSLDatabase('ssl')
    return host_database.get_hostnames()


def update_host_info(host):
    host_database = SSLDatabase('ssl')
    host_database.update_host_info(host)


def update_ssl_info(ssl):
    host_database = SSLDatabase('ssl')
    host_database.update_ssl_info(ssl)


def add_domains():
    case_domains = CaseDatabase('case').get_domains()
    ssl_database = SSLDatabase('ssl')
    ssl_domains = ssl_database.get_domains()
    not_in_ssl_domains = [item for item in case_domains if
                          item['domain'] not in [entry['domain'] for entry in ssl_domains]]
    if not_in_ssl_domains:
        for domain in not_in_ssl_domains:
            ssl_database.add_domain_info(domain)


def main():
    add_domains()
    hostnames = get_hostnames()
    for hostname in hostnames:
        host = Host(hostname)
        update_host_info(host)

        if host.protocol == 'HTTPS':
            ssl = SSLCertificate(hostname)
            update_ssl_info(ssl)


if __name__ == '__main__':
    main()
