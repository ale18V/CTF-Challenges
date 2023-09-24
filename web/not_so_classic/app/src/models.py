import time
import os
from flask import current_app
from flask_login import UserMixin, current_user
from werkzeug.datastructures import FileStorage
from . import db
from . import utils


class User(UserMixin):
    def __init__(self, id: int, username: str, password: str) -> None:
        self.id = id
        self.username = username
        self.password = password
        super().__init__()

    def get_id(self):
        return str(self.id)

    def getUploadsFolder(self):
        return os.path.join(current_app.static_folder, "uploads", self.get_id())


class Users(object):
    @staticmethod
    def resultRowToUser(res: db.sqlite3.Row):
        return User(res['id'], res['username'], res['password'])

    @staticmethod
    def get(id: int | str) -> User | None:
        con = db.getConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM USERS WHERE id = :id",
                    {"id": id})
        res = cur.fetchone()
        if res:
            return Users.resultRowToUser(res)

    @staticmethod
    def getByUsername(username: str):
        con = db.getConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM USERS WHERE username = :username",
                    {"username": username})
        res = cur.fetchone()
        if res:
            return Users.resultRowToUser(res)

    @staticmethod
    def add(username: str, password: str) -> User | None:
        con = db.getConnection()
        cur = con.cursor()
        try:
            id = time.time_ns()
            cur.execute("INSERT INTO USERS VALUES (?, ?, ? )",
                        (id, username, password))
            con.commit()
            added_user = User(id, username, password)
            os.mkdir(added_user.getUploadsFolder())
            return added_user
        except Exception as error:
            current_app.logger.error(error)
            con.rollback()


class Upload(object):
    def __init__(self, id: bytes, uploader: User) -> None:
        self.id = id
        self.uploader = uploader

    def getAbsolutePath(self) -> str:
        return os.path.join(current_app.static_folder, "uploads", self.uploader.get_id(), self.id.hex())

    def getHTMLPath(self) -> str:
        return os.path.join("/static", "uploads", self.uploader.get_id(), self.id.hex())


class Uploads(object):
    @staticmethod
    def resultRowToUpload(res: db.sqlite3.Row, uploader: User | None = None):
        return Upload(res['id'], uploader or Users.get(res['uploader_id']))

    @staticmethod
    def get(id: bytes, uploader: User) -> Upload | None:
        con = db.getConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM UPLOADS WHERE id = ? and uploader_id = ?",
                    (id, uploader.id))
        res = cur.fetchone()
        if res:
            return Uploads.resultRowToUpload(res)

    @staticmethod
    def getByUploader(uploader: User):
        con = db.getConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM UPLOADS WHERE uploader_id = ?",
                    (uploader.id))
        return [Uploads.resultRowToUpload(res, uploader) for res in cur.fetchall()]

    @staticmethod
    def add(file: FileStorage, uploader: User = current_user) -> Upload | None:
        # If the same file has already been uploaded we don't store it again
        # Probability of md5 collision within files uploaded by the same user is extremely low
        id = utils.md5FileHash(file)
        if upload := Uploads.get(id, uploader):
            return upload

        con = db.getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO UPLOADS VALUES(?, ?)", (id, uploader.id))
        con.commit()
        result = Upload(id, uploader)
        file.save(result.getAbsolutePath())
        return result


class Post(object):
    def __init__(self, id: int, title: str, content: str, creator: User, image: Upload) -> None:
        self.id = id
        self.title = title
        self.content = content
        self.creator = creator
        self.image = image

    def shareWith(self, user: User) -> bool:
        con = db.getConnection()
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO POST_SHARES VALUES(:post_id, :user_id)", {
                        "post_id": self.id, "user_id": user.id})
            con.commit()
            return cur.rowcount != 0
        except Exception as error:
            current_app.logger.error(error)
            con.rollback()
            return False


class Posts(object):
    @staticmethod
    def resultRowToPost(res: db.sqlite3.Row, creator: User | None = None, image: Upload | None = None):
        creator = creator or Users.get(res['creator_id'])
        image = image or Upload(res['image_id'], creator)
        return Post(res['id'], res['title'], res['content'], creator, image)

    @staticmethod
    def getById(id: int) -> Post | None:
        con = db.getConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM POSTS WHERE id=:id", {"id": id})
        res = cur.fetchone()
        if res:
            return Posts.resultRowToPost(res)

    @staticmethod
    def getByCreator(creator: User) -> list[Post]:
        con = db.getConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM POSTS WHERE posts.creator_id=:creator_id",
                    {"creator_id": creator.id})
        return [Posts.resultRowToPost(res, creator=creator) for res in cur.fetchall()]

    @staticmethod
    def getSharedWith(user: User) -> list[Post]:
        con = db.getConnection()
        cur = con.cursor()
        cur.execute("""SELECT * FROM POSTS p JOIN USERS u ON p.creator_id = u.id 
                    WHERE p.id IN (SELECT post_id FROM POST_SHARES WHERE user_id = :user_id)""",
                    {"user_id": user.id})
        return list(map(
            lambda res: Posts.resultRowToPost(
                res,
                creator=User(res['creator_id'],
                             res['username'], res['password'])
            ),
            cur.fetchall()
        ))

    @staticmethod
    def add(title: str, content: str, creator: User, image: Upload) -> Post | None:
        con = db.getConnection()
        cur = con.cursor()
        try:
            id = time.time_ns()
            cur.execute(
                "INSERT INTO POSTS VALUES(?, ?, ?, ?, ?)",
                (id, title, content, creator.id, image.id))
            con.commit()
            return Post(id, title, content, creator, image)
        except Exception as error:
            current_app.logger.error(error)
            con.rollback()

    @staticmethod
    def delete(id: int) -> bool:
        con = db.getConnection()
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM POSTS WHERE id = :id", {"id": id})
            con.commit()
            return cur.rowcount != 0
        except Exception as error:
            current_app.logger.error(error)
            con.rollback()
            return False
