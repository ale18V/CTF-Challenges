from secrets import token_urlsafe
from flask import Flask, current_app, request, session
from flask_login import current_user, login_required


class CSRFException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

# Adds CSRF protection to forms accessible by logged-in users.
def init_app(app: Flask):
    
    # Thanks ChatGPT
    def endpointRequiresLogin(endpoint: str):
        view_func = current_app.view_functions.get(request.endpoint)
        return hasattr(view_func, '__wrapped__') and isinstance(view_func.__wrapped__, type(login_required))

    @app.before_request
    def check_form():
        if request.method == 'POST' and request.form and endpointRequiresLogin(request.endpoint):
            csrf = request.form.get('csrf', type=str)
            if csrf is None or not session.get('csrf', default=None) or session['csrf'] != csrf:
                raise CSRFException('Hacker detected')
