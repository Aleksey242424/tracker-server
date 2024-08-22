from flask import Blueprint,redirect,url_for


bp = Blueprint(
    name="errors",
    import_name=__name__
)

@bp.app_errorhandler(401)
def error_401(code):
    response = redirect(url_for("auth.login"))
    response.headers["WWW-Authenticated"] = "Bearer"
    return response

@bp.app_errorhandler(404)
def error_404(code):
    return "Page Not Found",404