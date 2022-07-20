import sqlite3
from datetime import *


def get_people_id():
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM login_id')
    records = cursor.fetchall()
    cursor.close()
    return len(records)


def add_money2(user_id):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    stock_add = 500
    cursor.execute(f'UPDATE login_id SET money = ? WHERE id = ?', (stock_add, user_id))
    db.commit()


def remove_money(user_id):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    stock_add = 0
    cursor.execute(f'UPDATE login_id SET money = ? WHERE id = ?', (stock_add, user_id))
    db.commit()


def check_money(user_id):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    db_money = cursor.execute(f"SELECT * FROM login_id WHERE id = {user_id}")
    row = cursor.fetchone()
    return row

def add_money_db(user_id, user_add_money):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    db_money = cursor.execute(f"SELECT * FROM login_id WHERE id = {user_id}")
    row = cursor.fetchone()
    stock_add = row[4]
    res = stock_add + user_add_money
    cursor.execute(f'UPDATE login_id SET money = ? WHERE id = ?', (res, user_id))
    db.commit()

def remove_money_db(user_id, user_add_money):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    db_money = cursor.execute(f"SELECT * FROM login_id WHERE id = {user_id}")
    row = cursor.fetchone()
    stock_add = row[4]
    res = stock_add - user_add_money
    cursor.execute(f'UPDATE login_id SET money = ? WHERE id = ?', (res, user_id))
    db.commit()



def check_all_info(user_id):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM login_id WHERE id = {user_id}")
    row = cursor.fetchone()
    return row