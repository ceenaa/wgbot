import sqlite3

DB = None


def connect_to_db():
    global DB
    DB = sqlite3.connect("database.db")


def create_table():
    with DB:
        DB.execute("""
        CREATE TABLE IF NOT EXISTS peers
                     (name TEXT PRIMARY KEY,
                     public_key TEXT NOT NULL,
                     pre_shared_key TEXT NOT NULL,
                     endpoint TEXT NOT NULL,
                     allowed_ips TEXT NOT NULL,
                     latest_handshake TEXT NOT NULL,
                     transfer INTEGER NOT NULL,
                     active INTEGER NOT NULL)
        """
                   )


def init():
    connect_to_db()
    create_table()
