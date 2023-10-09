import datetime
import re
import threading

from database import Database
from database_schema import SSLCert
from host import Host
from ssl_certificate import SSLCertificate


class SSLDatabase(Database):
    def __init__(self, database_name):
        super(SSLDatabase, self).__init__(database_name)
        self.lock = threading.Lock()

    def get_hostnames(self):
        hostnames = []
        certs = self.session.query(SSLCert)
        for cert in certs:
            hostnames.append(cert.domain_name)
        return hostnames

    def update_host_info(self, host: Host):
        with self.lock:
            self.session.query(SSLCert).filter(SSLCert.domain_name == host.hostname).update(
                {
                    'exception': 'N' if host.is_connectable else 'Y',
                    'protocol': host.protocol,
                    'last_update_time': datetime.datetime.now()
                }
            )
            self.session.commit()

    def update_ssl_info(self, ssl: SSLCertificate):
        with self.lock:
            self.session.query(SSLCert).filter(SSLCert.domain_name == ssl.hostname).update(
                {
                    'applied_date': ssl.cert_starts,
                    'expire_date': ssl.cert_expires,
                    'issued_to': ssl.issued_to,
                    'last_update_time': datetime.datetime.now()
                }
            )
            self.session.commit()

    def get_domains(self):
        domains = []
        certs = self.session.query(SSLCert)
        for cert in certs:
            domain = self.extract_domain(cert.domain_name)
            if domain:
                entry = {'app': cert.project, 'domain': domain}
                domains.append(entry)
        return domains

    def extract_domain(self, url):
        pattern = r'(?:https?://)?([^/?#]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None

    def add_domain_info(self, data):
        with self.lock:
            new_ssl_cert = SSLCert(domain_name=data['domain'], project=data['app'], ignore_alert='N',
                                   last_update_time=datetime.datetime.now())
            self.session.add(new_ssl_cert)
            self.session.commit()
