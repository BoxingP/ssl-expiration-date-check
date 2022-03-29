from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SSLCert(Base):
    __tablename__ = 'domain_ssl_cert'
    id = Column(Integer, primary_key=True)
    domain_name = Column(String)
    applied_date = Column(Time)
    expire_date = Column(Time)
    last_update_time = Column(Time)
