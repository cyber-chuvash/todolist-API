from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)

    lists = relationship('List', back_populates='owner', cascade='all, delete-orphan')

    def get_api_repr(self, include_email=False):
        api_repr = {
            "id": self.id,
            "username": self.username,
        }
        if include_email:
            api_repr['email'] = self.email
        return api_repr

