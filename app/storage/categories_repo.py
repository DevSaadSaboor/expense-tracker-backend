from app.storage.db import get_connection
from psycopg2.extras import RealDictCursor

def create_category(user_id,name):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
        insert into categories(user_id,name)
        values(%s,%s)
        returning id,user_id,name,created_at
    """,(user_id,name))
        connection.commit()

        # data = cur.lastrowid
    #     cur.execute("""
    # select id,user_id,name,created_at from categories where id = %s
    # """,(data,))
        row = cur.fetchone()
        return row if row else None
    except Exception:
        connection.rollback()
        raise
    finally:
        cur.close()
        connection.close()


def get_categories_by_user(user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(""" 
        select id,user_id,name,created_at from categories where user_id = %s order by name asc 
        """,(user_id,))

        rows= cur.fetchall()
        return rows if rows else None
    finally:
        cur.close()
        connection.close()

def get_category_by_id(category_id,user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
        select id,user_id,name,created_at from categories where id = %s and user_id = %s 
        """,(category_id,user_id))

        row = cur.fetchone()
        return row if row else None
    finally:
        cur.close()
        connection.close()

def update_category(category_id,user_id,fields):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    set_parts  = []
    values = []

    for key,value in fields.items():
        set_parts.append(f"{key} = %s")
        values.append(value)
    set_clause = ",".join(set_parts)
    try:
        cur.execute(f"""
        UPDATE categories SET {set_clause} where id = %s and user_id = %s
        """,tuple(values) + (category_id,user_id))

        connection.commit()
        result = cur.rowcount
        if result == 0:
            return None
        
        cur.execute("""
        select id,user_id,name,created_at from categories where id = %s and user_id = %s
        """,(category_id,user_id))

        row = cur.fetchone()
        return row if row else None
    except Exception:
        connection.rollback()
        raise
    finally:
        cur.close()
        connection.close()

def delete_category( category_id,user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
    DELETE from categories where id = %s AND user_id = %s
    """,(category_id,user_id))
    connection.commit()

    if cur.rowcount > 0:
        return True
    return False



