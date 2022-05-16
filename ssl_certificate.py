import datetime
import socket
import ssl

import OpenSSL


class SSLCertificate(object):
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.cert_starts = None
        self.cert_expires = None
        self.issued_to = None
        self.get_ssl_valid_date()

    def get_ssl_valid_date(self, port: int = 443):
        ssl_date_fmt = r'%Y%m%d%H%M%S%z'

        domain = self.get_domain()
        context = ssl.SSLContext()
        with socket.create_connection((domain, port)) as conn:
            with context.wrap_socket(conn, server_hostname=domain) as sock:
                certificate = sock.getpeercert(True)
                cert = ssl.DER_cert_to_PEM_cert(certificate)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
                self.cert_starts = datetime.datetime.strptime(x509.get_notBefore().decode('utf-8'), ssl_date_fmt)
                self.cert_expires = datetime.datetime.strptime(x509.get_notAfter().decode('utf-8'), ssl_date_fmt)
                self.issued_to = x509.get_subject().commonName

    def get_domain(self):
        return self.hostname.split('/')[0]
