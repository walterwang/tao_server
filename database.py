import sqlite3 as sql
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username,password):
    con = sql.connect("database.db")

    cur = con.cursor()

    cur.execute("select username from users where username=?", (username,))
    data = cur.fetchone()

    if data:
        print("username taken")
    else:
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,generate_password_hash(password)))
        con.commit()
    con.close()


def get_user(username, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchone()
    if users:
        if check_password_hash(users[1], password):
            print("authenticated")
        else:
            print("wrong password!")
    else:
        print("username does not exist")
    con.close()


if __name__ == '__main__':
    register_user("walter", "123456")
    get_user("walter", "123456")