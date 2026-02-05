from typing import Dict
from app.storage.db import get_connection
from psycopg2.extras import RealDictCursor


def create_user(name:str,email:str,password_hash):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
    """
    INSERT into USERS (name,email,password_hash)
    values(%s,%s,%s)
    RETURNING id,name,email,created_at;
    """,(name,email,password_hash)
        )
        row = cur.fetchone()
        connection.commit()
        return dict(row)
    except Exception:
        connection.rollback()
        raise
    finally:
        cur.close()


def list_users(limit:int,offset:int):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
    select id,name,email,created_at from users order by id
    limit %s offset %s
    """,(limit,offset))

        rows = cur.fetchall()
        # result = []
        # for row in rows:
        #     convert  = dict(row)
        #     result.append(convert)
        # return result
        return rows
    except Exception:
        connection.rollback()
        raise
    finally:
        cur.close()

def get_user_by_id(user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
    """
    SELECT  id,name,email,created_at from users where id = %s 
    """,(user_id,)
    )
        row = cur.fetchone()
        return row if row else None
    finally:
        cur.close()


def update_user(user_id: int, fields: dict):
    if not fields:
        return None
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    set_parts = []
    values = []
    for key, value in fields.items():
        set_parts.append(f"{key} = %s")
        values.append(value)
    set_clause = ", ".join(set_parts)
    values.append(user_id)
    try:
        cur.execute(f"""
        UPDATE users SET {set_clause} WHERE id = %s

        """,
        tuple(values)
    )
        connection.commit()
        cur.execute(
        """
        SELECT id, name, email, created_at
        FROM users
        WHERE id = %s
        """,
        (user_id,)
    )

        row = cur.fetchone()
        return row if row else None
    except Exception:
        connection.rollback()
        raise
    finally:
        cur.close()


def delete_user(user_id : int):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
        delete from users where id = %s
        """,(user_id,))
        connection.commit()
        if cur.rowcount == 0:
            return False
        return True
    except Exception:
        connection.rollback()
        raise
    finally:
        cur.close()

def get_user_by_lognin(email):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
        select id,password_hash from users where email = %s 
        """,(email,))
        rows = cur.fetchone()
        return rows if rows else None
    except Exception:
        raise
    finally:
        cur.close()








