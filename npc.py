from sqlalchemy import Column, Integer, String
from base import Base


class Npc(Base):
    """ NPC Class """

    __tablename__ = "npcs"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    age = Column(String(200), nullable=False)
    alias = Column(String(200), nullable=False)
    country = Column(String(200), nullable=False)
    position = Column(String(200), nullable=False)
    specialization = Column(String(200), nullable=False)
    docs_link = Column(String(200), nullable=False)

    def __init__(self, name, age, alias, country, position, specialization, docs_link):
        """ Creates a new NPC record """

        self.name = name
        self.age = age
        self.alias = alias
        self.country = country
        self.position = position
        self.specialization = specialization
        self.docs_link = docs_link

    def to_dict(self):
        """ Converts the NPC record to a Python dictionary """
        new_dict = {"id": self.id,
                    "name": self.name,
                    "age": self.age,
                    "alias": self.alias,
                    "country": self.country,
                    "position": self.position,
                    "specialization": self.specialization,
                    "docs_link": self.docs_link}
        return new_dict
