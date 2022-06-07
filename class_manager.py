from classes import Classes

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ClassManager:
    """ Manager of class records """

    def __init__(self, db_name):

        if db_name is None or db_name == "":
            raise ValueError("DB Name cannot be undefined")

        engine = create_engine("sqlite:///" + db_name)
        self._db_session = sessionmaker(bind=engine)

    def add_class(self, class_name, armor_type, weapon_type, initial_equip, perks):
        """ Adds a single class """
        session = self._db_session()

        self._validate_string_input(class_name, 'Class Name')
        self._validate_string_input(armor_type, 'Armor Type')
        self._validate_string_input(weapon_type, 'Weapon Type')
        self._validate_string_input(initial_equip, 'Initial Equipment')
        self._validate_string_input(perks, 'Perks')
        new_class = Classes(class_name, armor_type, weapon_type, initial_equip, perks)
        session.add(new_class)
        session.commit()

        session.close()

    def delete_class(self, class_name):
        """ Deletes a single employee based on the id """

        self._validate_string_input(class_name, 'Class Name')

        session = self._db_session()

        del_class = session.query(Classes).filter(Classes.class_name == class_name).first()

        if del_class is None:
            session.close()
            raise ValueError("Class Name does not exist")

        session.delete(del_class)
        session.commit()

        session.close()

    def get_all_classes(self):
        """ Returns a list of all employees """

        session = self._db_session()

        class_list = session.query(Classes).all()

        session.close()

        return class_list

    def get_class(self, class_name):
        """ Returns a list of all employees """

        session = self._db_session()

        get_class = session.query(Classes).filter(Classes.class_name == class_name).first()

        session.close()

        return get_class

    @staticmethod
    def _validate_string_input(validate_string, text):
        """Validates for string inputs"""
        if type(validate_string) != str or validate_string == "" or validate_string is None:
            raise ValueError("{} must be defined and valid".format(text))
