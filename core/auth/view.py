from flask import Blueprint,render_template,request
from .form import RegisterForm,LoginForm
from .utils import RegisterAuth,LoginAuth,check_auth


bp = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth"
)

@bp.before_request
def check_failed_login():
    print(request.args)

@bp.route("/register/",methods={"GET","POST"})
@check_auth
def register():
    form = RegisterForm()
    if request.method == "POST":
        form_data = request.form.to_dict()
        return RegisterAuth(form_data).main()
    else:
        return render_template("auth/register.html",form = form)
    

@bp.route("/login/",methods={"GET","POST"})
@check_auth
def login():
    form = LoginForm()
    if request.method == "POST":
        form_data = request.form.to_dict()
        return LoginAuth(form_data=form_data).main()
    else:
        return render_template("auth/login.html",form=form)
        

