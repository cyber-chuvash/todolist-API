from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
