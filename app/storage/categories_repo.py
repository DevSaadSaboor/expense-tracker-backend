from app.storage.db import get_connection
import sqlite3
def row_to_dict(row:sqlite3):
    return dict(row)

def create_category(user_id,name):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    insert into categories(user_id,name)
    values(?,?)
""",(user_id,name))
    connection.commit()
    data = cur.lastrowid
    cur.execute("""
    select id,user_id,name,created_at from categories where id = ?
""",(data,))
    row = cur.fetchone()
    if row is None:
        return None
    return row_to_dict(row) 


def get_categories_by_user(user_id):
    connection = get_connection()
    cur = connection.cursor()

    cur.execute(""" 
    select id,user_id,name,created_at from categories where user_id = ? order by name asc 
    """,(user_id,))

    rows= cur.fetchall()
    if not rows:
        return None
    return [row_to_dict(row) for row in rows]

def get_category_by_id(category_id,user_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    select id,user_id,name,created_at from categories where id = ? and user_id = ? 
    """,(category_id,user_id))

    row = cur.fetchone()
    
    if row is None:
        return None
    return row_to_dict(row)

def update_category(category_id,user_id,fields):
    connection = get_connection()
    cur = connection.cursor()
    set_parts  = []
    values = []

    for key,value in fields.items():
        set_parts.append(f"{key} = ?")
        values.append(value)
    set_clause = ",".join(set_parts)
    
    cur.execute(f"""
    UPDATE categories SET {set_clause} where id = ? and user_id = ?
    """,tuple(values) + (category_id,user_id))

    connection.commit()
    result = cur.rowcount
    if result == 0:
        return None
    
    cur.execute("""
    select id,user_id,name,created_at from categories where id = ? and user_id = ?
    """,(category_id,user_id))

    row = cur.fetchone()
    if row is None:
        return None

    return dict(row)

def delete_category( category_id,user_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    DELETE from categories where id = ? AND user_id = ?
    """,(category_id,user_id))
    connection.commit()

    if cur.rowcount > 0:
        return True
    return False



