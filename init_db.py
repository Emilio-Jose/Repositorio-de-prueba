import sqlite3

conn = sqlite3.connect('usuarios.db')
c = conn.cursor()
c.execute('''
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    password_hash TEXT NOT NULL
  )
''')
conn.commit()
conn.close()
