from flask import Flask, Response


def init_app(app: Flask):
    @app.after_request
    def csp(response: Response):
        response.headers['Content-Security-Policy'] = '; '.join([
            "script-src 'self' https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"            
        ])
        return response
    pass