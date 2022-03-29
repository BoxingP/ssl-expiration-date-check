import json
import os
from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_schema import SSLCert

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
Session = sessionmaker()


class Database(object):
    def __init__(self):
        engine = self.create_engine()
        Session.configure(bind=engine)
        self.session = Session()

    def create_engine(self):
        with open(CONFIG_PATH, 'r', encoding='UTF-8') as file:
            config = json.load(file)
        db_config = config['database']
        adapter = db_config['adapter']
        host = db_config['host']
        port = db_config['port']
        database = db_config['database']
        user = db_config['user']
        password = db_config['password']
        db_uri = f'{adapter}://{user}:%s@{host}:{port}/{database}' % quote(password)
        return create_engine(db_uri, echo=False)

    def get_hosts(self):
        hosts = []
        certs = self.session.query(SSLCert)
        for cert in certs:
            hosts.append(cert.domain_name)
        return hosts
