import datetime
from urllib.parse import quote

from decouple import config as decouple_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_schema import SSLCert
from host import Host
from ssl_certificate import SSLCertificate

Session = sessionmaker()


class Database(object):
    def __init__(self):
        engine = self.create_engine()
        Session.configure(bind=engine)
        self.session = Session()

    def create_engine(self):
        adapter = decouple_config('SSL_DATABASE_ADAPTER')
        host = decouple_config('SSL_DATABASE_HOST')
        port = decouple_config('SSL_DATABASE_PORT')
        database = decouple_config('SSL_DATABASE_DATABASE')
        user = decouple_config('SSL_DATABASE_USER')
        password = decouple_config('SSL_DATABASE_PASSWORD')
        db_uri = f'{adapter}://{user}:%s@{host}:{port}/{database}' % quote(password)
        return create_engine(db_uri, echo=False)

    def get_hostnames(self):
        hostnames = []
        certs = self.session.query(SSLCert)
        for cert in certs:
            hostnames.append(cert.domain_name)
        return hostnames

    def update_host_info(self, host: Host):
        self.session.query(SSLCert).filter(SSLCert.domain_name == host.hostname).update(
            {
                'exception': 'N' if host.is_connectable else 'Y',
                'protocol': host.protocol,
                'last_update_time': datetime.datetime.now()
            }
        )
        self.session.commit()

    def update_ssl_info(self, ssl: SSLCertificate):
        self.session.query(SSLCert).filter(SSLCert.domain_name == ssl.hostname).update(
            {
                'applied_date': ssl.cert_starts,
                'expire_date': ssl.cert_expires,
                'issued_to': ssl.issued_to,
                'last_update_time': datetime.datetime.now()
            }
        )
        self.session.commit()
