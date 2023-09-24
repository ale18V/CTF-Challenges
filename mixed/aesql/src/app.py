from flask import Flask, render_template, request, redirect, url_for, make_response, g
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode
import sqlite3
import os
import string
import random

DB_PATH = os.getenv("DB_PATH")

KEY = os.urandom(16)
ALLOWED_CHARS = string.ascii_letters + string.digits + "!@#$%^&*()_-+={[}]|\:;<,>.?/"

app = Flask(__name__)
connection = sqlite3.connect(DB_PATH, check_same_thread=False)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


@app.route("/")
def index():
    session = request.cookies.get("session")
    name = None
    tasks = None
    if session:
        try:
            name, password = decrypt_session(session)
        except Exception as e:
            print(e)
            return 'Hacker detected'

        # Admin won't be able to login but whatever
        if name == "admin":
            return 'Hacker detected'
        
        tasks = cursor.execute(
            f"SELECT id, title, content, completed FROM tasks WHERE owner = '{name}'").fetchall()

    return render_template('index.html', title="AESQL", username=name, tasks=tasks)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title="Register")
    elif request.method == 'POST':
        # Make sure that name and password are passed as params
        name, password = request.form.get('name'), request.form.get('password')
        if name is None or password is None:
            return "Username or password missing"

        # Check if username already exists
        if check_user_exists(name):
            return "Username already exists"

        # Check that username is valid. We don't want SQLi here ;)
        if not username_is_valid(name):
            return f"Allowed characters are '{ALLOWED_CHARS}'"

        # Add new user to db
        cursor.execute("INSERT INTO USERS VALUES (:name, :password)", {
                       'name': name, 'password': password})
        return redirect(url_for("login"))

    return ''


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Login")
    elif request.method == 'POST':
        # Make sure that name and password are passed as params
        name, password = request.form.get('name', type=str), request.form.get('password',type=str)
        if name is None or password is None:
            return "Username or password missing"

        # Check the login is valid
        if not check_user_exists(name, password):
            return "Wrong username or password"
        iv = os.urandom(16)
        aes = AES.new(key=KEY, mode=AES.MODE_CBC, iv=iv)
        cookies = {
            'name': aes.encrypt(pad(name.encode(), block_size=16)).hex(),
            'password': aes.encrypt(pad(password.encode(), block_size=16)).hex(),
            'iv': iv.hex()
        }

        response = make_response(redirect(url_for("index")))
        response.set_cookie(
            key='session',
            value=urlsafe_b64encode(json.dumps(cookies).encode())
        )
        return response

    return ''


@app.route("/new", methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template('new.html')
    elif request.method == 'POST':
        # Check that user is logged in
        session = request.cookies.get("session")
        if not session:
            return 'You must be logged in in order to add a new task'

        # Check that the user is valid
        name, password = decrypt_session(session)
        if not check_user_exists(name, password):
            return 'Hacker detected'

        # Add new task
        title, content = request.form.get('title', type=str), request.form.get('content', type=str)
        if title is None or content is None:
            return 'Invalid request'

        cursor.execute("INSERT INTO TASKS(title, content, completed, owner) VALUES(:title, :content, false, :owner)",
                       {'title': title, 'content': content, 'owner': name})

        return redirect(url_for("index"))


@app.post("/tasks/<int:id>")
def update_task_completed(id: int):
    if not check_task_exists(id):
        return make_response("Non existent task", 400)
    
    completed = request.form.get('completed', default=None, type=bool)
    if completed is None:
        return make_response("Invalid params", 400)
    

    cursor.execute("UPDATE TASKS SET completed = :completed WHERE id = :id", 
                   {'completed' : completed, 'id' : id})
    return redirect(url_for("index"))


def decrypt_session(session: str) -> tuple[str, str]:
    enctypted_cookies = json.loads(urlsafe_b64decode(session))
    iv = bytes.fromhex(enctypted_cookies['iv'])
    aes = AES.new(key=KEY, mode=AES.MODE_CBC, IV=iv)
    name = unpad(aes.decrypt(bytes.fromhex(
        enctypted_cookies['name'])), block_size=16).decode()
    password = unpad(aes.decrypt(bytes.fromhex(
        enctypted_cookies['password'])), block_size=16).decode()
    return name, password


def check_user_exists(name: str, password: str | None = None) -> bool:
    query = "SELECT * FROM users WHERE name = :name "
    params = {'name': name}

    if password is not None:
        query += "AND password = :password"
        params['password'] = password

    return True if cursor.execute(query, params).fetchone() else False

def check_task_exists(id: int) -> bool:
    return True if cursor.execute("SELECT 1 FROM tasks WHERE id = :id", {'id': id}).fetchone() else False 

def username_is_valid(name: str) -> bool:
    # Check that the characters used are allowed
    return all( x in ALLOWED_CHARS for x in name)

if __name__ == "__main__":
    adminpwd =  ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16) )
    cursor.execute(f"INSERT INTO USERS VALUES('admin', '{adminpwd}')")
    cursor.execute("INSERT INTO TASKS(title, content, completed, owner) VALUES ('flag', :flag, false, 'admin')", {'flag': os.getenv('FLAG')})
    app.run(host="0.0.0.0", port='7000')
