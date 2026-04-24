import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        os.getenv("DATABASE_URL"), cursor_factory=psycopg2.extras.RealDictCursor
    )

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
