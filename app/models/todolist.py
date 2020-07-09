from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class List(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), index=True)

    owner = relationship('User', back_populates='lists')
    cards = relationship('Card', back_populates='list', cascade='all, delete-orphan')

    def get_api_repr(self, include_cards=False):
        api_repr = {
            "id": self.id,
            "title": self.title,
        }
        if include_cards:
            api_repr['cards'] = list(map(lambda card: card.get_api_repr(), self.cards))
        return api_repr
