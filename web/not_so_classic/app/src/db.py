import sqlite3
from flask import current_app, g
from flask import Flask


def getConnection() -> sqlite3.Connection:
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(current_app.config['DATABASE_PATH'], detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = sqlite3.Row
        g.db = db
    return db

def init_app(app: Flask):
    @app.teardown_appcontext
    def closeConnection(exception):
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()