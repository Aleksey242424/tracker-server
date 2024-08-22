from flask import session,redirect,url_for
from functools import wraps
from core.auth.utils import jwt_decode
from flask_wtf import FlaskForm
from .schem import Project as ProjectSchem
from uuid import uuid4
from core.system_db.crud import ProjectCRUD

def current_user(token) -> dict:
    return jwt_decode(token=token)

def check_owner(func):
    @wraps(func)
    def check(*a,**kw):
        if not current_user(token = session.get("auth"))["is_owner"]:
            return redirect(url_for("tracker.worker"))
        return func(*a,*kw)
    return check

def check_worker(func):
    @wraps(func)
    def check(*a,**kw):
        if current_user(token = session.get("auth"))["is_owner"]:
            return redirect(url_for("tracker.owner"))
        return func(*a,*kw)
    return check


def init_form(form:FlaskForm,**data):
    for k,v in data.items():
        form.__getattribute__(k).data = v
    return form

class Project:
    def __init__(self,form_data:dict):
        self.project = self.init_project_data(form_data=form_data)
        self.project_crud = ProjectCRUD

    def create_project(self,owner_id:int):
        self.project.owner = owner_id
        self.project_crud.add(
            token = self.project.token,
            title=self.project.title,
            description=self.project.description,
            owner_id=self.project.owner
        )


    def init_project_data(self,form_data:dict):
        try:
            form_data.__delitem__("csrf_token")
            form_data.__delitem__("create")
        except AttributeError:
            pass
        finally:
            return ProjectSchem(
                token = uuid4().hex,
                title=form_data["title"],
                description=form_data["description"]
            )
