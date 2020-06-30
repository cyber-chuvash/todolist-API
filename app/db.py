from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models import Base

engine = create_engine('sqlite:///tmp/db.sqlite', echo=True)
Session = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all(engine)
