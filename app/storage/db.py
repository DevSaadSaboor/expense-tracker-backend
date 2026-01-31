import sqlite3 
from pathlib import Path


DB_path = Path(__file__).resolve().parents[2] /"data"/ "expense_tracker.db"

connection = None


def get_connection():
    global connection

    DB_path.parent.mkdir(parents=True, exist_ok=True)
    if connection is None:
        connection = sqlite3.connect(DB_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")

    return connection


def create_table():

    connection = get_connection()
    cur = connection.cursor()


    cur.execute(
    """
    create TABLE if not EXISTS users(
    id INTEGER PRIMARY key AUTOINCREMENT,
    name text not null,
    email text not null UNIQUE,
    created_at  datetime not null DEFAULT CURRENT_TIMESTAMP
    )
    """
    )


    cur.execute(
    """
    create table if not EXISTS categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER not NULL,
    name TEXT not NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id,name),
    FOREIGN KEY(user_id)
    REFERENCES users(id)    
    on DELETE RESTRICT
    )

    """
    )
    cur.execute(
    """
    create table if not EXISTS expenses(
    id INTEGER PRIMARY key AUTOINCREMENT,
    user_id INTEGER not null,
    category_id INTEGER,
    amount REAL not null,
    note TEXT,
    spend_at date not null,
    created_at datetime not null DEFAULT CURRENT_TIMESTAMP,

    FOREIGN key(user_id)
    REFERENCES users(id)
    on DELETE RESTRICT,
    
    FOREIGN key(category_id)
    REFERENCES categories(id)
    on DELETE SET NULL
    )

    """
    )

    connection.commit()