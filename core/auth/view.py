from flask import Blueprint

bp = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth"
)


@bp.route("/",methods={"GET","POST"})
def register():
    return ""