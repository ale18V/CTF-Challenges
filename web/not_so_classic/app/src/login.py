from flask import url_for
from flask_login import LoginManager
from .models import Users

login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message = "Please login to visit the requested page"
login_manager.login_message_category = "info"
@login_manager.user_loader
def loadUser(id: str | int):
    return Users.get(id)