from flask import Flask,Response
from os import makedirs
from instance.config import setting


def create_app(config = setting):
    app = Flask(
        import_name=__name__,
        template_folder="templates",
        static_folder="static"
    )
    
    app.config.from_object(config)

    from core.system_db.utils import init_db

    app.cli.add_command(init_db)

    try:
        makedirs(app.instance_path)
    
    except OSError:
        pass

    from core.auth.view import bp as auth_bp

    app.register_blueprint(auth_bp)

    @app.after_request
    def add_security_headers(response:Response):
        response.headers["Strict-Transport-Security"] = "max-age=999999"
        response.headers["X-Content-Type-Security"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self' script-src 'unsafe-inline' 'self'"
        return response

    return app
