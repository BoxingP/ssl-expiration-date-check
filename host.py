import ssl
from http.client import HTTPSConnection, HTTPConnection
from urllib.parse import urlparse


class Host(object):
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.protocol = None
        self.is_connectable = None
        self.check_host()

    def check_host(self):
        is_http = self.check_http_url()
        is_https = self.check_https_url()

        if is_https:
            self.protocol = 'HTTPS'
            self.is_connectable = True
        else:
            if is_http:
                self.protocol = 'HTTP'
                self.is_connectable = True
            else:
                self.is_connectable = False

    def check_https_url(self):
        https_url = f'https://{self.hostname}'
        try:
            https_url = urlparse(https_url)
            connection = HTTPSConnection(https_url.netloc, timeout=5)
            connection.request('HEAD', https_url.path)
            if connection.getresponse():
                return True
            else:
                return False
        except ssl.CertificateError as error:
            return True
        except Exception as error:
            return False

    def check_http_url(self):
        http_url = f'http://{self.hostname}'
        try:
            http_url = urlparse(http_url)
            connection = HTTPConnection(http_url.netloc)
            connection.request('HEAD', http_url.path)
            if connection.getresponse():
                return True
            else:
                return False
        except Exception as error:
            return False
