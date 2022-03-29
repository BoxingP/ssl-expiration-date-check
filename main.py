from database import Database
from ssl_certificate import SSLCertificate


def get_hosts():
    host_database = Database()
    return host_database.get_hosts()


def main():
    hosts = get_hosts()
    for host in hosts:
        ssl = SSLCertificate(host)
        print(ssl.hostname)
        print(ssl.host_status)
        print(ssl.cert_starts)
        print(ssl.cert_expires)
        print(ssl.cert_remains)


if __name__ == '__main__':
    main()
