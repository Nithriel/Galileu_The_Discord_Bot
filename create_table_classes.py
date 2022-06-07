import sqlite3

conn = sqlite3.connect('classes.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE classes
          (id INTEGER PRIMARY KEY ASC, 
           class_name VARCHAR(200) NOT NULL,
           armor_type VARCHAR(200) NOT NULL,
           weapon_type VARCHAR(200) NOT NULL,
           initial_equip VARCHAR(200) NOT NULL,
           perks VARCHAR(200) NOT NULL
           )
          ''')

conn.commit()
conn.close()
