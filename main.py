from database import Database
from host import Host
from ssl_certificate import SSLCertificate


def get_hostnames():
    host_database = Database()
    return host_database.get_hostnames()


def main():
    hostnames = get_hostnames()
    for hostname in hostnames:
        host = Host(hostname)
        print(host.hostname)
        print(host.is_connectable)
        print(host.protocol)

        if host.protocol == 'HTTPS':
            ssl = SSLCertificate(hostname)
            print(ssl.cert_starts)
            print(ssl.cert_expires)
            print(ssl.issued_to)


if __name__ == '__main__':
    main()
