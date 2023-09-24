from flask import Flask, render_template_string, request
from markupsafe import escape
from src.csrf import CSRFException

def init_app(app : Flask):
    @app.errorhandler(404)
    def page_not_found(error):
        page = request.path
        return render_template_string("""<!DOCTYPE html>
                                      <html>
                                      <head><title>404 Not Found</title></head>
                                      <body>
                                        <h1>Not Found</h1>
                                      <p>The page %s was not found</p>
                                      <p>Use this <a href="{{ url_for('main.home') }}">link</a> to go back to the home page</p>
                                      </body>
                                      </html>""" % escape(page)), 404
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template_string("""<!DOCTYPE html>
                                      <html>
                                      <head><title>403 Forbidden</title></head>
                                      <body>
                                        <h1>Not Found</h1>
                                      <p>You don't have access to this page. Go somewhere else.</p>
                                      <p>Use this <a href="{{ url_for('main.home') }}">link</a> to go back to the home page</p>
                                      </body>
                                      </html>"""), 403
    
    @app.errorhandler(CSRFException)
    def csrfexception(error):
        return render_template_string("""<!DOCTYPE html>
                                      <html>
                                      <head><title>CSRF Error</title></head>
                                      <body>
                                        <h1>CSRF Error</h1>
                                      <p>The server was not able to verify that the request was legit.</p>
                                      <p>You can visit <a href="{{ url_for('user.login') }}">this link</a> to log in again</p>
                                      <p><b>ERROR:</b> %s</p>
                                      </body>
                                      </html>""" % error), 403