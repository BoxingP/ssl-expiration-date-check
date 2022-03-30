from database import Database
from host import Host
from ssl_certificate import SSLCertificate


def get_hostnames():
    host_database = Database()
    return host_database.get_hostnames()


def update_host_info(host):
    host_database = Database()
    host_database.update_host_info(host)


def update_ssl_info(ssl):
    host_database = Database()
    host_database.update_ssl_info(ssl)


def main():
    hostnames = get_hostnames()
    for hostname in hostnames:
        host = Host(hostname)
        update_host_info(host)

        if host.protocol == 'HTTPS':
            ssl = SSLCertificate(hostname)
            update_ssl_info(ssl)


if __name__ == '__main__':
    main()
