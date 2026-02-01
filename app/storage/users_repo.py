from typing import Optional,List,Dict
import sqlite3
from app.storage.db import get_connection

def row_to_dict(row:sqlite3):
    return dict(row)

def create_user(name:str,email:str,password_hash):
    connection = get_connection()
    cur = connection.cursor()

    cur.execute(
    """
    INSERT into USERS (name,email,password_hash)
    values(%s,%s,%s);
    """,(name,email,password_hash)
    )
    connection.commit()
    newuser_id = cur.lastrowid
    cur.execute(
    """ 
    SELECt id,name,email,created_at from users where id = %s
    """,(newuser_id,)
    )
    row = cur.fetchone()
    if row is None:
        return None
    return dict(row)

def list_users(limit:int,offset:int):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    select id,name,email,created_at from users order by id
    limit %s offset %s
    """,(limit,offset))

    rows = cur.fetchall()
    result = []
    for row in rows:
        convert  = dict(row)
        result.append(convert)
    return result

def get_user_by_id(user_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute(
    """
    SELECT  id,name,email,created_at from users where id = %s 
    """,(user_id,)
    )
    row = cur.fetchone()
    if not row:
        return None
    return dict(row)

def update_user(user_id: int, fields: dict):
    if not fields:
        return None
    connection = get_connection()
    cursor = connection.cursor()
    set_parts = []
    values = []
    for key, value in fields.items():
        set_parts.append(f"{key} = %s")
        values.append(value)
    set_clause = ", ".join(set_parts)
    values.append(user_id)
    cursor.execute(
        f"""
        UPDATE users
        SET {set_clause}
        WHERE id = %s
        """,
        tuple(values)
    )
    connection.commit()
    cursor.execute(
        """
        SELECT id, name, email, created_at
        FROM users
        WHERE id = %s
        """,
        (user_id,)
    )

    row = cursor.fetchone()
    return dict(row) if row else None


def delete_user(user_id : int):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    delete from users where id = %s
    """,(user_id,))

    connection.commit()

    if cur.rowcount == 0:
        return False
    return True

def get_user_by_lognin(email):
    connection = get_connection()
    cur = connection.cursor()

    cur.execute("""
    select id,password_hash from users where email = %s 
    """,(email,))
    rows = cur.fetchone()
    return dict(rows) if rows else None









