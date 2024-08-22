from flask import Blueprint,session,redirect,url_for,render_template,request
from .utils import current_user,check_owner,check_worker,init_form,Project
from core.auth.utils import login_required
from .form import ProfileWorker,CreateProject

bp = Blueprint(
    name="tracker",
    import_name=__name__,
    url_prefix="/tracker"
)


@bp.route("/",methods={"GET","POST"})
@login_required
def main():
    user = current_user(token = session.get("auth"))
    if user["is_owner"]:
        return redirect(url_for("tracker.owner"))
    return redirect(url_for("tracker.worker"))


@bp.route("/owner/<int:id>/",methods={"GET","POST"})
@login_required
@check_owner
def owner(id):
    if request.method == "POST":
        Project(request.form.to_dict()).create_project(id)
    form = CreateProject()
    return render_template("tracker/main_owner.html",form=form)
    

@bp.route("/worker/",methods={"GET","POST"})
@login_required
@check_worker
def worker():
    user = current_user(token = session.get("auth"))
    return render_template("tracker/main_worker.html")



@bp.route("/worker/<id>/",methods={"GET","POST"})
@login_required
@check_worker
def profile_worker(id):
    user = current_user(token = session.get("auth"))
    form = ProfileWorker()
    return render_template("tracker/profile_worker.html",name=user["name"],form=form)


@bp.route("/owner/<int:id>/",methods={"GET","POST"})
@login_required
@check_owner
def profile_owner(id):
    user = current_user(token = session.get("auth"))
    form = init_form(
        ProfileWorker(),
        name=user["name"]
    )
    return render_template("tracker/profile_owner.html",name=user["name"],form=form)