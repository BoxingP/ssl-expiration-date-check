import concurrent.futures

from decouple import config as decouple_config

from case_database import CaseDatabase
from host import Host
from ssl_certificate import SSLCertificate
from ssl_database import SSLDatabase


def add_domains():
    case_domains = CaseDatabase('case').get_domains()
    ssl_database = SSLDatabase('ssl')
    ssl_domains = ssl_database.get_domains()
    not_in_ssl_domains = [item for item in case_domains if
                          item['domain'] not in [entry['domain'] for entry in ssl_domains]]
    if not_in_ssl_domains:
        for domain in not_in_ssl_domains:
            ssl_database.add_domain_info(domain)


def process_host(hostname, host_database):
    host = Host(hostname)
    host_database.update_host_info(host)

    if host.protocol == 'HTTPS':
        ssl = SSLCertificate(hostname)
        host_database.update_ssl_info(ssl)


def main():
    add_domains()
    host_database = SSLDatabase('ssl')
    hostnames = host_database.get_hostnames()

    max_threads = decouple_config('THREAD_MAX', cast=int)
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(process_host, hostname, host_database): hostname for hostname in hostnames}
        concurrent.futures.wait(futures)


if __name__ == '__main__':
    main()
