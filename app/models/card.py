from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('lists.id'), index=True)

    text = Column(String, nullable=False)
    description = Column(String)
    is_done = Column(Boolean, nullable=False, default=False)

    list = relationship('List', back_populates='cards')

    def get_api_repr(self):
        return {
            "id": self.id,
            "text": self.text,
            "description": self.description,
            "is_done": self.is_done
        }

