import sqlite3
from flask import g, url_for, current_app
from subprocess import Popen
import socket
import os
import signal

def open_connection_and_get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(current_app.config['DBPATH'])
        db.row_factory = sqlite3.Row
        g.db = db
    return db


def get_posts_of(username: str) -> list[dict]:
    db = open_connection_and_get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, title, content FROM POSTS WHERE creator=:username",
        {"username": username}
    )
    return cursor.fetchall()


def get_post_by_id(post_id: int) -> dict | None:
    db = open_connection_and_get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM POSTS WHERE id=:post_id",
                   {"post_id": post_id})
    return cursor.fetchone()


def start_admin(post_id: int):
    if get_post_by_id(post_id) is None:
        return
    report_url = f"http://classic:{os.getenv('CHALLENGE_PORT')}{url_for('view_post', post_id=post_id)}"
    with open(current_app.config['FIFO_PATH'], mode="a") as fifo:
        fifo.write(f"{report_url}\n")
        os.kill(int(current_app.config['DAEMON_PID']), signal.SIGUSR1)
    
