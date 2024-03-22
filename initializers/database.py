import sqlite3

DB = None


def connect_to_db():
    global DB
    DB = sqlite3.connect("database.db")
    DB.autocommit = False
