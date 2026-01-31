from app.storage.db import get_connection
import sqlite3
def row_to_dict(row:sqlite3):
    return dict(row)

# done
def create_expense(user_id,category_id,amount,note,spend_at):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    Insert into expenses (user_id,category_id,amount,note,spend_at)
    values(?,?,?,?,?)
    """,(user_id,category_id,amount,note,spend_at)
    )
    connection.commit()
    result = cur.lastrowid
    cur.execute("""
    select id,user_id,category_id,amount,note,spend_at,created_at from expenses where id = ?             
    """,(result,))
    row = cur.fetchone()
    return row_to_dict(row)

# done
def get_expenses_by_user(user_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    Select id,user_id,category_id,amount,note,spend_at,created_at from expenses where user_id = ? order by amount asc
    """,(user_id,))
    rows = cur.fetchall()
    return [row_to_dict(row) for row in rows]

# done 
def get_expenses_by_id(user_id,expense_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    Select id,user_id,category_id,amount,note,spend_at,created_at from expenses where id = ? and user_id = ?
    """,(expense_id,user_id))
    rows = cur.fetchone()
    if not rows:
        return None
    return row_to_dict(rows)

# Done
def get_expense_by_category(user_id,category_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    Select id,user_id,category_id,amount,note,spend_at,created_at 
    from expenses 
    where user_id = ? and category_id = ?
    order by spend_at desc
    """,(user_id,category_id))
    rows = cur.fetchall()
    return [row_to_dict(row) for row in rows]

# Done
def get_expenses_with_category(user_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    select expenses.id,expenses.user_id,expenses.amount,expenses.note,expenses.spend_at,expenses.created_at,expenses.category_id,
    categories.name as category_name
    from expenses
    join categories
    on expenses.category_id = categories.id
    where expenses.user_id = ?
    """,(user_id,))
    rows = cur.fetchall()
    return [dict(row) for row in rows]

# Done
def get_category_totals(user_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    select categories.id, categories.name as Category_name, sum(expenses.amount) as total_amount 
    FROM expenses
    JOIN categories
    on expenses.category_id = categories.id
    where user_id = ?
    group by categories.id,categories.name
    """,(user_id,))
    rows = cur.fetchall()
    return [dict(row) for row in rows]

# Done
def get_category_month_total(user_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    select strftime('%Y-%m', spend_at) as month,
    sum(amount) as total
    from expenses
    where user_id = ?
    group by strftime('%Y-%m', spend_at)
    order by month
    """,(user_id,))
    rows = cur.fetchall()
    return [dict(row) for row in rows]

# Done
def get_monthly_category_totals(user_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    SELECT categories.name, strftime('%Y-%m', spend_at) as month, sum(expenses.amount) as total_amount 
    from expenses
    join categories
    on categories.id = expenses.category_id
    where expenses.user_id = ? 
    GROUP by categories.name, strftime('%Y-%m', spend_at)
    """,(user_id,)) 
    rows = cur.fetchall()
    return [dict(row) for row in rows]

# remeaing 
def get_monthly_totals_between_dates(user_id, start_date, end_date):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    select strftime('%Y-%m', spend_at) as month , sum(amount) as total_amount
    from expenses
    where expenses.user_id = ? AND
    expenses.spend_at BETWEEN ? and ? 
    GROUP by strftime('%Y-%m', spend_at)
    ORDER by month
    """,(user_id,start_date,end_date))
    rows = cur.fetchall()
    return [dict(row) for row in rows]

# done
def get_expenses_paginated(user_id, limit, offset):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    select id,user_id,category_id,amount,note,spend_at,created_at
    from expenses 
    where expenses.user_id = ? 
    order by expenses.created_at DESC
    limit ?
    OFFSET ? 
    """,(user_id,limit,offset))
    rows = cur.fetchall()
    return [dict(row) for row in rows]

# done
def update_expense(expense_id,user_id,fields):
    connection = get_connection()
    cur = connection.cursor()
    keys = []
    values = []
    for key,value in fields.items():
            
            keys.append(f"{key} = ?" )
            values.append(value)
    set_clause = ",".join(keys)
    cur.execute(f"""
    update expenses set {set_clause} where id = ? and user_id =?  
    """,tuple(values) + (expense_id,user_id))
    connection.commit()
    result = cur.rowcount 
    if result == 0 :
        return None
    cur.execute("""
    Select id,user_id,category_id,amount,note,spend_at,created_at from expenses where id = ? and user_id = ?
    """,(expense_id,user_id))
    row = cur.fetchone()
    if row is None :
        return None
    return row_to_dict(row)

# done
def delete_expense(expense_id,user_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("""
    delete from expenses where id = ? and user_id = ?
    """,(expense_id,user_id))
    connection.commit()
    if cur.rowcount > 0:
        return True
    return False
