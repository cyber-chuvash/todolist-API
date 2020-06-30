from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship

from models.base import Base


class ListItem(Base):
    __tablename__ = 'list_items'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('lists.id'))

    text = Column(String, nullable=False)
    description = Column(String)
    is_done = Column(Boolean, nullable=False)

    list = relationship('List', back_populates='items')

