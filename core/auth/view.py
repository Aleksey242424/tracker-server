from flask import Blueprint,render_template,request
from .form import RegisterForm
from .utils import RegisterAuth

bp = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth"
)


@bp.route("/register/",methods={"GET","POST"})
def register():
    if request.method == "POST":
        form_data = request.form.to_dict()
        RegisterAuth(form_data).main()
    else:
        form = RegisterForm()
        return render_template("auth/register.html",form = form)