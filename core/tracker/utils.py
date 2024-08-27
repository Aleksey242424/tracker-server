from flask import session,redirect,url_for,abort
from functools import wraps
from core.auth.utils import jwt_decode
from flask_wtf import FlaskForm
from .schem import Project as ProjectSchem
from uuid import uuid4,UUID
from core.system_db.crud import ProjectCRUD,TrackerInfo,TrackerLink
from datetime import datetime

def current_user(token) -> dict:
    return jwt_decode(token=token)

def check_owner(func):
    @wraps(func)
    def check(id:int,token=None):
        user = current_user(token = session.get("auth"))
        if not user["is_owner"]:
            return redirect(url_for("tracker.worker",id=user["id"]))
        if token is not None:
            return func(id,token)
        return func(id)
    return check

def check_worker(func):
    @wraps(func)
    def check(id:int,token=None):
        user = current_user(token = session.get("auth"))
        if user["is_owner"]:
            return redirect(url_for("tracker.owner",id=user["id"]))
        if token is not None:
            return func(id,token)
        return func(id)
    return check


def init_form(form:FlaskForm,**data):
    for k,v in data.items():
        form.__getattribute__(k).data = v
    return form

class Project:
    def __init__(self,person_id:int):
        self.project_crud = ProjectCRUD
        self.tracker_info_crud = TrackerInfo
        self.tracker_link_crud = TrackerLink
        self.person_id = person_id
        

    def create_project(self,form_data:dict):
        project = self.init_project_data(form_data=form_data)
        self.project_crud.add(
            token = project.token,
            title=project.title,
            description=project.description,
            owner_id=project.owner
        )

    def get_projects_owner(self) -> list:
        return self.project_crud.get_all_for_owner(owner_id=self.person_id)
    
    def get_projects_worker(self) -> list:
        return self.tracker_link_crud.get_all(person_id=self.person_id)
    
    def get_project_by_token(self,token:UUID) -> tuple|None:
        project = self.project_crud.get_by_token(
            token=token,
            person_id=self.person_id
            )
        if project is not None:
            return project
        abort(404)

    def get_workers_by_project(self,token:UUID):
        return self.tracker_info_crud.get_workers_by_token(
            token=token
        )
    
    def get_is_active_workers(self,token:UUID):
        return self.tracker_info_crud.get_is_active_workers(
            token=token
        )
            
    
    def add_project(self,token:UUID) -> None:
        self.tracker_info_crud.add(
            person_id=self.person_id,
            token=token
        )
        self.tracker_link_crud.add(
            worker_id = self.person_id,
            token = token
        )
    
    def update_time(self,token:UUID,time:datetime):
        self.tracker_info_crud.update_time(
            person_id=self.person_id,
            token=token,
            time=time
        )

    def update_is_active(self,token:UUID,active:bool):
        self.tracker_info_crud.update_is_active(
            person_id=self.person_id,
            token=token,
            is_active=active
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
                description=form_data["description"],
                owner = self.person_id
            )
