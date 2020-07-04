from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models import Base

Session = None


def init_db(app):
    global Session
    engine = create_engine(app.config['DB_CONNECT_URL'], echo=app.config.get('DB_ECHO', False))
    Session = scoped_session(sessionmaker(bind=engine))

    Base.metadata.create_all(engine)
