import os
import os.path as path
from flask import Blueprint, abort, current_app, flash, redirect, render_template_string, request, render_template, send_file, session, url_for
from flask_login import login_required, login_user, current_user
from markupsafe import escape
from src.models import Uploads, Users, Posts
from secrets import token_urlsafe
from . import utils

mainbp = Blueprint('main', __name__)
userbp = Blueprint('user', __name__)
postbp = Blueprint('post', __name__)
adminbp = Blueprint('admin', __name__)


@mainbp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("post.view"))
    else:
        return render_template("home.jinja")


@userbp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("user/register.jinja")
    elif request.method == 'POST':
        username = request.form.get("username", type=str)
        password = request.form.get("password", type=str)

        if username is None or password is None:
            abort(400)

        if username == "" or password == "":
            flash("Provide username and password", category="error")
            return redirect(url_for('user.register'))

        user = Users.add(username, password)
        if not user:
            flash("Username already taken", category="error")
            return redirect(url_for('user.register'))
        else:
            current_app.logger.info(
                "Registered user %s with username %s" % (user.id, user.username))
            return redirect(url_for('user.login'))


@userbp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.jinja')
    elif request.method == 'POST':
        username = request.form.get("username", type=str)
        password = request.form.get("password", type=str)

        if username is None or password is None:
            abort(400)

        user = Users.getByUsername(username)
        if user is None or user.password != password:
            flash("Invalid credentials", category="error")
            return redirect(url_for("user.login"))
        else:
            login_user(user)
            session['csrf'] = token_urlsafe(16)
            return redirect(url_for("main.home"))


@postbp.route("/view")
@login_required
def view():
    if request.args.get('shared'):
        result = render_template(
            "post/shared_view.jinja", posts=Posts.getSharedWith(current_user))
    else:
        result = render_template(
            "post/view.jinja", posts=Posts.getByCreator(current_user))
    return result


@postbp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "GET":
        return render_template("post/new.jinja")
    elif request.method == "POST":
        title = request.form.get("title", default=None, type=str)
        content = request.form.get("content", default=None, type=str)
        image = request.files.get("image")
        if title is None or content is None or image is None:
            return abort(400)

        if title == "" or content == "":
            flash("The title or the content field can't be empty", category="error")
            return redirect(url_for("post.new"))
        elif not image.filename:
            flash("Please upload an image", category="error")
            return redirect(url_for("post.new"))

        upload = Uploads.add(image)
        post = Posts.add(title, content, current_user, upload)
        current_app.logger.info("User %s created post %s", current_user.id, post.id)
        return redirect(url_for("post.view"))


@postbp.route("/delete", methods=["POST"])
@login_required
def delete():
    post_id = request.form.get("id", default=None, type=int)
    if post_id is None:
        return abort(400)

    post = Posts.getById(post_id)
    if post is None or post.creator.id != current_user.id:
        return abort(404)

    if Posts.delete(post_id):
        current_app.logger.info("User %s deleted post %s", current_user.id, post.id)

    return redirect(url_for("post.view"))


@postbp.route("/share", methods=["POST"])
@login_required
def share():
    post_id = request.form.get("id", default=None, type=int)
    recipient_username = request.form.get("recipient", default=None, type=str)
    if post_id is None or recipient_username is None:
        return abort(400)

    recipient = Users.getByUsername(recipient_username)
    if recipient is None:
        flash(f"Post can't be shared with user {recipient_username} because the user does not exist.",
              category="error")
    elif not Posts.getById(post_id).shareWith(recipient):
        flash(f"Post can't be shared (already shared with {recipient_username}?)",
              category="error")
    else:
        current_app.logger.info(
            "User %s shared post %s with %s",
            current_user.id, post_id, recipient.id)

    return redirect(url_for("post.view"))


@adminbp.get("/logs")
@login_required
def download_logs():
    if current_user.username != "admin":
        return abort(403)
    return send_file(current_app.config['LOG_PATH'], mimetype="text/plain")


@adminbp.route("/report", methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'GET':
        return render_template("admin/report.jinja")
    elif request.method == 'POST':
        reported_url = request.form.get('url', type=str)
        if reported_url is None:
            return abort(400)
        elif not utils.isValidURL(reported_url):
            flash("Invalid URL", category="error")
            return redirect(url_for('admin.report'))
        else:
            try:
                utils.startAdmin(reported_url)
                flash("Page reported successfully!", category="info")
                current_app.logger.info(
                    "User %s reported the following url %s", current_user.id, reported_url)
            except Exception as error:
                flash(str(error), category="error")
                current_app.logger.error(error)
            finally:
                return redirect(url_for("admin.report"))
