from urllib.parse import quote

from decouple import config as decouple_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database(object):
    def __init__(self, database_name):
        self.database_name = database_name
        engine = self.create_engine()
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_engine(self):
        name = self.database_name.upper()
        adapter = decouple_config(f'{name}_DATABASE_ADAPTER')
        host = decouple_config(f'{name}_DATABASE_HOST')
        port = decouple_config(f'{name}_DATABASE_PORT')
        database = decouple_config(f'{name}_DATABASE_DATABASE')
        user = decouple_config(f'{name}_DATABASE_USER')
        password = decouple_config(f'{name}_DATABASE_PASSWORD')
        db_uri = f'{adapter}://{user}:%s@{host}:{port}/{database}' % quote(password)
        return create_engine(db_uri, echo=False)
