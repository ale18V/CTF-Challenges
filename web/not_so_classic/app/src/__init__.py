from flask import Flask, render_template
from flask_env import MetaFlaskEnv
import jinja2.sandbox
from . import logging
from . import db
from .login import login_manager
from . import errors
from . import csp
from . import csrf
from . import challenge


class Configuration(metaclass=MetaFlaskEnv):
    # Loads APP_ environment variables into the app's config
    ENV_PREFIX = "APP_"
    ENV_LOAD_ALL = True


class JinjaEnvironment(jinja2.sandbox.SandboxedEnvironment):
    # Simply wraps jinja's sandboxed environment so that it can be used with flask
    def __init__(self, app: Flask, **options) -> None:
        if "loader" not in options:
            options["loader"] = app.create_global_jinja_loader()
        jinja2.sandbox.SandboxedEnvironment.__init__(self, **options)
        self.app = app


def create_app(configuration=Configuration):
    app = Flask(__name__)
    app.config.from_object(configuration)

    # We have high security standards ;)
    app.jinja_options["autoescape"] = True
    app.jinja_environment = JinjaEnvironment

    # Init extensions and db
    db.init_app(app)
    login_manager.init_app(app)
    logging.init_app(app)
    errors.init_app(app)
    csp.init_app(app)
    csrf.init_app(app)
    challenge.init_app(app)

    # Blueprints
    from .routes import userbp
    app.register_blueprint(userbp, url_prefix="/user")
    from .routes import postbp
    app.register_blueprint(postbp, url_prefix="/post")
    from .routes import mainbp
    app.register_blueprint(mainbp, url_prefix="")
    from .routes import adminbp
    app.register_blueprint(adminbp, url_prefix="/admin")
    return app
