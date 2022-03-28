import datetime
import os
import socket
import ssl

HOSTS_FILE = os.path.join(os.path.dirname(__file__), 'hosts.txt')


def get_hosts():
    with open(HOSTS_FILE, 'r', encoding='UTF-8') as file:
        hosts = [line.strip() for line in file.readlines()]
    return hosts


def ssl_valid_datetime(hostname: str):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname
    )
    conn.settimeout(3.0)
    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    start = datetime.datetime.strptime(ssl_info['notBefore'], ssl_date_fmt)
    expired = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    ssl_date = (start, expired)
    return ssl_date


def ssl_valid_time_remaining(hostname: str):
    valid_time = ssl_valid_datetime(hostname)
    return valid_time[1] - datetime.datetime.utcnow()


def test_host(hostname: str, buffer_days: int = 30):
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
        if will_expire_in < datetime.timedelta(days=0):
            return f'{hostname} cert will expired'
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
