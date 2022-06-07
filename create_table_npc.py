import sqlite3

conn = sqlite3.connect('npcs.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE npcs
          (id INTEGER PRIMARY KEY ASC,
           name VARCHAR(200) NOT NULL,
           age VARCHAR(200) NOT NULL,
           alias VARCHAR(200) NOT NULL,
           country VARCHAR(200) NOT NULL,
           position VARCHAR(200) NOT NULL,
           specialization VARCHAR(200) NOT NULL,
           docs_link VARCHAR(200) NOT NULL
           )
          ''')

conn.commit()
conn.close()