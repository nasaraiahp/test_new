from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base

DATABASE_URL = "sqlite:///files.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    from models import FileRecord
    Base.metadata.create_all(bind=engine)
