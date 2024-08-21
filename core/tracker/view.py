from flask import Blueprint,session
from core.auth.utils import jwt_decode

bp = Blueprint(
    name="tracker",
    import_name=__name__,
    url_prefix="/tracker"
)


@bp.route("/",methods={"GET","POST"})
def main():
    token = session["auth"]
    user = jwt_decode(token)
    return user["name"]

