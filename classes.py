from sqlalchemy import Column, Integer, String
from base import Base


class Classes(Base):
    """ Classes Class """

    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    class_name = Column(String(200), nullable=False)
    armor_type = Column(String(200), nullable=False)
    weapon_type = Column(String(200), nullable=False)
    initial_equip = Column(String(200), nullable=False)
    perks = Column(String(200), nullable=False)

    def __init__(self, class_name, armor_type, weapon_type, initial_equip, perks):
        """ Creates a new Class record """

        self.class_name = class_name
        self.armor_type = armor_type
        self.weapon_type = weapon_type
        self.initial_equip = initial_equip
        self.perks = perks

    def to_dict(self):
        """ Converts the Class record to a Python dictionary """

        new_dict = {"id": self.id,
                    "class_name": self.class_name,
                    "armor_type": self.armor_type,
                    "weapon_type": self.weapon_type,
                    "initial_equip": self.initial_equip,
                    "perks": self.perks}

        return new_dict
