from app.storage.db import get_connection
from psycopg2.extras import RealDictCursor

def create_expense(user_id,category_id,amount,note,spend_at):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
        Insert into expenses (user_id,category_id,amount,note,spend_at)
        SELECT %s,id,%s,%s,%s
        from categories 
        where id = %s  and user_id = %s
        RETURNING *
        """,(user_id, amount, note, spend_at, category_id, user_id)
        )
        row = cur.fetchone()    
        connection.commit()
        return row
    # cur.execute("""
    # select id,user_id,category_id,amount,note,spend_at,created_at from expenses where id = %s             
    # """,(result,))
    except Exception:
        connection.rollback()
        raise
    finally:
        cur.close()
        connection.close()


def get_expenses_by_user(user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
        Select id,user_id,category_id,amount,note,spend_at,created_at from expenses where user_id = %s order by spend_at desc
        """,(user_id,))
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        connection.close()

def get_expenses_by_id(user_id,expense_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
        Select id,user_id,category_id,amount,note,spend_at,created_at from expenses where id = %s and user_id = %s
        """,(expense_id,user_id))
        rows = cur.fetchone()
        if not rows:
            return None
        return rows
    finally:
        cur.close()
        connection.close()


def get_expense_by_category(user_id,category_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
    Select id,user_id,category_id,amount,note,spend_at,created_at 
    from expenses 
    where user_id = %s and category_id = %s
    order by spend_at desc
    """,(user_id,category_id))
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        connection.close()


def get_expenses_with_category(user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
    select expenses.id,expenses.user_id,expenses.amount,expenses.note,expenses.spend_at,expenses.created_at,expenses.category_id,
    categories.name as category_name
    from expenses
    join categories
    on expenses.category_id = categories.id
    where expenses.user_id = %s
    """,(user_id,))
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        connection.close()

def get_category_totals(user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
    select categories.id, categories.name as Category_name, sum(expenses.amount) as total_amount 
    FROM expenses
    JOIN categories
    on expenses.category_id = categories.id
    where user_id = %s
    group by categories.id,categories.name
    """,(user_id,))
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        connection.close()

def get_category_month_total(user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
    select to_char(spend_at, 'YYYY-MM') as month,
    sum(amount) as total
    from expenses
    where user_id = %s
    group by to_char(spend_at, 'YYYY-MM')
    order by month
    """,(user_id,))
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        connection.close()

def get_monthly_category_totals(user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
    SELECT categories.name, to_char(spend_at,'YYYY-MM') as month, sum(expenses.amount) as total_amount 
    from expenses
    join categories
    on categories.id = expenses.category_id
    where expenses.user_id = %s 
    GROUP by categories.name, to_char(spend_at,'YYYY-MM')
    """,(user_id,)) 
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        connection.close()

def get_monthly_totals_between_dates(user_id, start_date, end_date):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
    select to_char(spend_at,'YYYY-MM') as month , sum(amount) as total_amount
    from expenses
    where expenses.user_id = %s AND
    expenses.spend_at BETWEEN %s and %s 
    GROUP by to_char(spend_at,'YYYY-MM')
    ORDER by month
    """,(user_id,start_date,end_date))
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        connection.close()
# done
def get_expenses_paginated(user_id, limit, offset):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
    select id,user_id,category_id,amount,note,spend_at,created_at
    from expenses 
    where expenses.user_id = %s 
    order by expenses.created_at DESC
    limit %s
    OFFSET %s 
    """,(user_id,limit,offset))
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        connection.close()
# done
def update_expense(expense_id,user_id,fields):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    keys = []
    values = []
    for key,value in fields.items():
            
            keys.append(f"{key} = %s" )
            values.append(value)
    set_clause = ",".join(keys)
    try:
        cur.execute(f"""
    update expenses set {set_clause} where id = %s and user_id =%s  
    RETURNING id,user_id,category_id,amount,note,spend_at,created_at
    """,tuple(values) + (expense_id,user_id))
        connection.commit()
        result = cur.rowcount 
        if result == 0 :
            return None
    # cur.execute("""
    # Select id,user_id,category_id,amount,note,spend_at,created_at from expenses where id = %s and user_id = %s
    # """,(expense_id,user_id))
        row = cur.fetchone()
        if row is None :
            return None
        return row
    finally:
        cur.close()
        connection.close()

def delete_expense(expense_id,user_id):
    connection = get_connection()
    cur = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
    delete from expenses where id = %s and user_id = %s
    """,(expense_id,user_id))
        connection.commit()
        if cur.rowcount > 0:
            return True
        return False
    except Exception:
        connection.rollback()
        raise
    finally:
        cur.close()
        connection.close()