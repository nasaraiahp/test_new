#defining the database models

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class FileRecord(Base):
    __tablename__ = 'files'
    
    file_id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    expiration = Column(DateTime, default=datetime.datetime.utcnow)
    downloads = Column(Integer, default=0)
    max_downloads = Column(Integer, default=5)
