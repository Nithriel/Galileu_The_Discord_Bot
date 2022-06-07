from npc import Npc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class NpcManager:
    """ Manager of npc records """

    def __init__(self, db_name):

        if db_name is None or db_name == "":
            raise ValueError("DB Name cannot be undefined")

        engine = create_engine("sqlite:///" + db_name)
        self._db_session = sessionmaker(bind=engine)

    def add_npc(self, name, age, alias, country, position, specialization, docs_link):
        """ Adds a single npc """
        session = self._db_session()

        self._validate_string_input(name, 'Name')
        self._validate_string_input(age, 'Age')
        self._validate_string_input(alias, 'Alias')
        self._validate_string_input(country, 'Country')
        self._validate_string_input(position, 'Position')
        self._validate_string_input(specialization, 'Specialization')
        self._validate_string_input(docs_link, "Docs Link")
        new_npc = Npc(name, age, alias, country, position, specialization, docs_link)
        session.add(new_npc)
        session.commit()

        session.close()

    def delete_npc(self, npc_name):
        """ Deletes a single npc based on the name """

        self._validate_string_input(npc_name, 'Name')

        session = self._db_session()

        del_npc = session.query(Npc).filter(Npc.name == npc_name).first()

        if del_npc is None:
            session.close()
            raise ValueError("NPC does not exist")

        session.delete(del_npc)
        session.commit()

        session.close()

    def get_all_npc(self):
        """ Returns a list of all employees """

        session = self._db_session()

        class_list = session.query(Npc).all()

        session.close()

        return class_list

    def get_npc(self, npc_name):
        """ Returns a list of all npcs """

        session = self._db_session()

        get_class = session.query(Npc).filter(Npc.name == npc_name).first()

        session.close()

        return get_class

    @staticmethod
    def _validate_string_input(validate_string, text):
        """Validates for string inputs"""
        if type(validate_string) != str or validate_string == "" or validate_string is None:
            raise ValueError("{} must be defined and valid".format(text))
