from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base
from .user import User
from .todolist import List
from .listitem import ListItem

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
