import io
from flask import Flask
from werkzeug.datastructures import FileStorage
from os import path, getenv
from .models import Users, Posts, Uploads


# Initial inserts into the DB
# Adds the admin user and his posts
def init_app(app: Flask):
    with app.app_context():
        admin = Users.add("admin", getenv('ADMIN_PASSWORD'))
        if admin:
            with open(path.join(app.static_folder, "images", "nasa.jpeg"), mode="rb") as f:
                dummyImage = FileStorage(f)
                upload = Uploads.add(dummyImage, uploader=admin)
                Posts.add(title="How I hacked NASA",
                          content=getenv("FLAG"),
                          creator=admin,
                          image=upload)