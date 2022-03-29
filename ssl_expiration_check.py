import datetime
import os
import socket
import ssl

import OpenSSL

HOSTS_FILE = os.path.join(os.path.dirname(__file__), 'hosts.txt')


def get_hosts():
    with open(HOSTS_FILE, 'r', encoding='UTF-8') as file:
        hosts = [line.strip() for line in file.readlines()]
    return hosts


def ssl_valid_datetime(hostname: str, port: int = 443):
    ssl_date_fmt = r'%Y%m%d%H%M%S%z'

    context = ssl.SSLContext()
    with socket.create_connection((hostname, port)) as conn:
        with context.wrap_socket(conn, server_hostname=hostname) as sock:
            certificate = sock.getpeercert(True)
            cert = ssl.DER_cert_to_PEM_cert(certificate)
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            cert_starts = datetime.datetime.strptime(x509.get_notBefore().decode('utf-8'), ssl_date_fmt)
            cert_expires = datetime.datetime.strptime(x509.get_notAfter().decode('utf-8'), ssl_date_fmt)
            return cert_starts, cert_expires


def ssl_valid_time_remaining(hostname: str):
    valid_time = ssl_valid_datetime(hostname)
    return valid_time[1] - datetime.datetime.now(datetime.timezone.utc)


def test_host(hostname: str, buffer_hours: int = 24, buffer_days: int = 30):
    try:
        will_expire_in = ssl_valid_time_remaining(hostname)
    except ssl.CertificateError as error:
        return f'{hostname} cert error {error}'
    except ssl.SSLError as error:
        return f'{hostname} cert error {error}'
    except socket.timeout as error:
        return f'{hostname} could not connect'
    except socket.gaierror as error:
        return f'{hostname} could not be reached'
    else:
        if will_expire_in <= datetime.timedelta(days=0):
            return f'{hostname} cert is expired'
        elif datetime.timedelta(hours=buffer_hours) > will_expire_in > datetime.timedelta(hours=0):
            return f'{hostname} cert will expired soon in {buffer_hours} hours'
        elif will_expire_in < datetime.timedelta(days=buffer_days):
            return f'{hostname} cert will expire in {will_expire_in}'
        else:
            return f'{hostname} cert is fine'


def main():
    hosts = get_hosts()
    for host in hosts:
        print(host)
        message = test_host(host)
        print(message)


if __name__ == '__main__':
    main()
