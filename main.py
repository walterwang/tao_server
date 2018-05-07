from flask import Flask, request, session, abort, redirect, flash, g
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
DATABASE = 'database.db'
import redis_client

@app.route('/')
def connect_server():
    return "Hello, world"

@app.route('/update_setup', methods = ['POST'])
def update_setup():
    setup_array = request.form['setup']
    if 'username' in session:
        con = get_db()
        cur = con.cursor()

        cur.execute("UPDATE users SET setup=? WHERE username=?", (setup_array,session['username']))
        con.commit()
        con.close()

        return '%s Setup commited'%session['username']
    else:
        return 'user not logged in'

@app.route('/find_game')
def find_game():
    if 'username' in session:
        con = get_db()
        cur = con.cursor()
        cur.execute("select setup from users where username=?", (session['username'],))
        setup = cur.fetchone()[0]
        redis_client.register_game(session['username'], setup)

        return 'user registered in game pool'
    else:
        return 'user not logged in'

@app.route('/check_game_ready')
def check_game_ready():
    if 'username' in session:
        if redis_client.get_gameid(session['username']):
            return "ready"
        else:
            return "find"

@app.route('/get_board_state')
def get_board_state():
    if 'username' in session:
        game_id = redis_client.get_gameid(session['username'])
        print("game_id", type(game_id))
        board = redis_client.get_board(int(game_id))
        return str(board)
@app.route('/get_player_id')
def get_player_id():
    if 'username' in session:
        return str(redis_client.get_turnplayer(session['username']))


@app.route('/get_game_moves')
def get_game_moves():
    if 'username' in session:
        game_id = redis_client.get_gameid(session['username'])
        move_lists = redis_client.get_moves(game_id)
        print(move_lists)
        return str(move_lists)

@app.route('/post_moves', methods=['POST'])
def post_moves():
    if 'username' in session:
        game_id = redis_client.get_gameid(session['username'])
        redis_client.add_moves(game_id, request.form['moves'])
        return("moves posted")
    return("not logged in")


@app.route('/get_setup')
def get_setup():
    if 'username' in session:
        con = get_db()
        cur = con.cursor()
        cur.execute("select setup from users where username=?", (session['username'],))
        setup = cur.fetchone()
        return setup
    else:
        return 'user not logged in'

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    con = get_db()
    cur = con.cursor()
    cur.execute("select username from users where username=?", (username,))
    data = cur.fetchone()

    if data:
        con.close()
        return("username taken")
    else:
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,generate_password_hash(password)))
        con.commit()
        con.close()
        return("registered")

@app.route('/login', methods = ['POST'])
def client_login():
    username = request.form['username']
    password = request.form['password']

    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username, ))
    data = cur.fetchone()
    con.close()

    if data:
        if check_password_hash(data[2], password):
            session['username'] = username

            return "authenticated %s"%username
        else:
            return "wrong password!"
    else:
        return "username does not exist"



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000)
