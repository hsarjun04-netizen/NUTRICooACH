import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# Delete old database
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("Old database deleted")

# Reinitialize
exec(open(os.path.join(os.path.dirname(__file__), 'init_db.py')).read())
