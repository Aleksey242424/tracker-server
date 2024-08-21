from flask import Blueprint,render_template,request
from .form import RegisterForm,LoginForm
from .utils import RegisterAuth,LoginAuth,check_auth


bp = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth"
)



@bp.route("/register/",methods={"GET","POST"})
@check_auth
def register():
    if request.method == "POST":
        form_data = request.form.to_dict()
        return RegisterAuth(form_data).main()
    else:
        form = RegisterForm()
        return render_template("auth/register.html",form = form)
    

@bp.route("/login/",methods={"GET","POST"})
@check_auth
def login():
    if request.method == "POST":
        form_data = request.form.to_dict()
        return LoginAuth(form_data=form_data).main()
    else:
        form = LoginForm()
        return render_template("auth/login.html",form=form)