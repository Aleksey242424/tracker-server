from flask import Blueprint

bp = Blueprint(
    name="tracker",
    import_name=__name__,
    url_prefix="/tracker"
)


@bp.route("/",methods={"GET","POST"})
def main():
    return ""