from flask import Flask, render_template, request, g, make_response, redirect, session, url_for, abort
import os
from .utils import *
from time import time

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config.from_mapping(
    DBPATH=os.getenv("DBPATH"),
    FIFO_PATH = os.getenv("FIFO_PATH"),
    DAEMON_PID = os.getenv("DAEMON_PID")
)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.get("/")
def index():
    username = session.get("username", default=None)
    if username is None:
        return render_template("index.html")
    return redirect(url_for("view_posts"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username", default=None, type=str)
        password = request.form.get("password", default=None, type=str)
        if username is None or password is None:
            return abort(404)

        db = open_connection_and_get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM USERS WHERE username=:username", {"username": username})
        if cursor.fetchone() is not None:
            return make_response(render_template("register.html", error="The username is already taken"), 409)
        
        cursor.execute(
            "INSERT INTO USERS VALUES(:username, :password)",
            {"username": username, "password": password}
        )
        db.commit()
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username", default=None, type=str)
        password = request.form.get("password", default=None, type=str)
        if username is None or password is None:
            return abort(404)

        db = open_connection_and_get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM USERS WHERE username=:username AND password=:password",
            {"username": username, "password": password})
        if cursor.fetchone() is None:
            return make_response(render_template("login.html", error="Invalid credentials"), 401)
            
        session['username'] = username
        return redirect(url_for("index"))


@app.route("/posts/new", methods=["GET", "POST"])
def new_post():
    username = session.get('username', default=None)
    if username is None:
        return redirect(url_for("register"))
    if request.method == "GET":
        return render_template("post/new.html")
    elif request.method == "POST":
        title = request.form.get("title", default=None, type=str)
        content = request.form.get("content", default=None, type=str)
        if title is None or content is None:
            return abort(422)
        db = open_connection_and_get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO POSTS(creator, title, content) VALUES(:username, :title, :content)",
            {"username": username, "title": title, "content": content}
        )
        db.commit()
        return redirect(url_for("index"))


@app.get("/posts/view")
def view_posts():
    username = session.get('username', default=None)
    if username is None:
        return redirect(url_for("register"))
    else:
        return render_template("post/view.html", posts=get_posts_of(username))


@app.get("/posts/view/<int:post_id>")
def view_post(post_id: int):
    username = session.get('username', default=None)
    if username is None:
        return redirect(url_for("register"))

    post = get_post_by_id(post_id)
    if post is None:
        return abort(404)
    elif post['creator'] == username or username == 'admin':
        return render_template("/post/view.html", posts=[post])
    else:
        return abort(404)


@app.post("/posts/delete")
def delete_post():
    username = session.get('username', default=None)
    if username is None:
        return redirect(url_for("register"))

    post_id = request.form.get("id", default=None, type=int)
    if post_id is None:
        return abort(422)

    db = open_connection_and_get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM POSTS WHERE id=:id AND creator=:username",
        {"id": post_id, "username": username}
    )
    if cursor.fetchone() is None:
        return abort(404)

    cursor.execute("DELETE FROM POSTS WHERE id=:id", {"id": post_id})
    db.commit()
    return redirect(url_for("view_posts"))


@app.post("/posts/share")
def share_post():
    username = session.get("username", default=None)
    if username is None:
        return redirect(url_for("register"))

    post_id = request.form.get("id", default=None, type=int)
    if post_id is None:
        return abort(422)
    start_admin(post_id)
    return redirect(url_for("view_posts"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("CHALLENGE_PORT"))
