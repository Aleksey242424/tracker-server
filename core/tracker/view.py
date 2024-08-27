from flask import Blueprint,session,redirect,url_for,render_template,request,jsonify
from .utils import current_user,check_owner,check_worker,init_form,Project
from core.auth.utils import login_required
from .form import ProfileWorker,CreateProject
from datetime import timedelta

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
        return redirect(url_for("tracker.owner",id=user["id"]))
    return redirect(url_for("tracker.worker",id=user["id"]))


@bp.route("/owner/<int:id>/",methods={"GET"})
@login_required
@check_owner
def owner(id):
    projects = Project(person_id=id).get_projects_owner()
    return render_template("tracker/main_owner.html",projects=projects,id=id)
    

@bp.route("/worker/<int:id>/",methods={"GET","POST"})
@login_required
@check_worker
def worker(id):
    project_instance = Project(person_id=id)
    if request.method == "POST":
        project_instance.add_project(request.form.get("token"))
        return redirect(url_for("tracker.worker",id=id))
    projects = project_instance.get_projects_worker()
    return render_template("tracker/main_worker.html",id=id,projects=projects)


@bp.route("/owner/<int:id>/create/",methods={"GET","POST"})
@login_required
@check_owner
def create_project(id):
    if request.method == "POST":
        Project(id).create_project(request.form.to_dict())
        return redirect(url_for("tracker.owner",id=id))
    form = CreateProject()
    return render_template("tracker/create_project.html",form=form,id=id)


@bp.route("/worker/<int:id>/project/<uuid:token>/update_time/",methods={"GET","PUT"})
@login_required
@check_worker
def update_time(id,token):
    time = list(map(int,request.args.get("time").split(":")))
    new_time = timedelta(hours = time[0],minutes=time[1],seconds=time[2]+1)
    Project(person_id=id).update_time(
        token=token,
        time=new_time
    )
    return jsonify(new_time = str(new_time))

@bp.route("/worker/<int:id>/project/<uuid:token>/is_active/",methods={"PUT"})
@login_required
@check_worker
def update_active(id,token):
    project = Project(person_id=id)
    if request.args.get("active"):
        project.update_is_active(token=token,
                                 active=True)
    else:
        project.update_is_active(token=token,
                                 active=False)
    return jsonify(message = "change active")

@bp.route("/owner/<int:id>/project/<uuid:token>/check_active/",methods={"GET"})
@login_required
@check_owner
def check_active_workers(id,token):
    states_workers = {}
    for data in Project(person_id=id).get_is_active_workers(token):
        states_workers[data[0]] = {
            "id":data[0],
            "state":data[1],
            "time":str(data[2])
        }
    return states_workers


@bp.route("/worker/<int:id>/project/<uuid:token>/")
@login_required
@check_worker
def project_worker(id,token):
    project = Project(person_id=id).get_project_by_token(token=token)
    return render_template("tracker/project_worker.html",id=id,project=project,token=token)

@bp.route("/owner/<int:id>/project/<uuid:token>/")
@login_required
@check_owner
def project_owner(id,token):
    workers = Project(person_id=id).get_workers_by_project(token=token)
    return render_template("tracker/project_owner.html",id=id,token=token,workers = workers)


@bp.route("/worker/<int:id>/profile/",methods={"GET","POST"})
@login_required
@check_worker
def profile_worker(id):
    user = current_user(token = session.get("auth"))
    form = ProfileWorker()
    return render_template("tracker/profile_worker.html",name=user["name"],form=form)


@bp.route("/owner/<int:id>/profile/",methods={"GET","POST"})
@login_required
@check_owner
def profile_owner(id):
    user = current_user(token = session.get("auth"))
    form = init_form(
        ProfileWorker(),
        name=user["name"]
    )
    return render_template("tracker/profile_owner.html",name=user["name"],form=form,id=id)