import datetime
import socket
import ssl

import OpenSSL


class SSLCertificate(object):
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.host_status = None
        self.cert_starts = None
        self.cert_expires = None
        self.cert_remains = None
        self.get_ssl_valid_date()

    def ssl_valid_datetime(self, port: int = 443):
        ssl_date_fmt = r'%Y%m%d%H%M%S%z'

        context = ssl.SSLContext()
        with socket.create_connection((self.hostname, port)) as conn:
            with context.wrap_socket(conn, server_hostname=self.hostname) as sock:
                certificate = sock.getpeercert(True)
                cert = ssl.DER_cert_to_PEM_cert(certificate)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
                self.cert_starts = datetime.datetime.strptime(x509.get_notBefore().decode('utf-8'), ssl_date_fmt)
                self.cert_expires = datetime.datetime.strptime(x509.get_notAfter().decode('utf-8'), ssl_date_fmt)
                self.cert_remains = self.cert_expires - datetime.datetime.now(datetime.timezone.utc)

    def get_ssl_valid_date(self):
        try:
            self.ssl_valid_datetime()
            self.host_status = 'connected'
        except ssl.CertificateError as error:
            self.host_status = f'{self.hostname} cert error {error}'
        except ssl.SSLError as error:
            self.host_status = f'{self.hostname} cert error {error}'
        except socket.timeout as error:
            self.host_status = 'unconnected'
        except socket.gaierror as error:
            self.host_status = 'unreachable'
        except ConnectionResetError as error:
            self.host_status = 'unreachable'
        except TimeoutError as error:
            self.host_status = 'unreachable'
