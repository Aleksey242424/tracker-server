from tests.cfgtest import *
import pytest
from flask import session,request
from core.tracker.utils import current_user
from core.auth.schem import User
from contextlib import nullcontext



class TestOwner:
    @pytest.mark.parametrize("name,password,expected",[
        ("TestOwner","123123",nullcontext()),
        ("UnknownTestOwner","123123",pytest.raises(TypeError))
    ])
    def test_create_project(self,client,name,password,expected):
        with client,expected:
            client.post("/auth/login/",data={
                    "name":name,
                    "password":password
                })
            user = current_user(token=session["auth"])
            
            assert client.post(f"/tracker/owner/{user.get('id')}/create/",data={"title":"test title","description":"test description"}).status_code == 200


    @pytest.mark.parametrize("name,password,new_name,new_email,expected",[
        ("TestOwner","123123","NewTestOwner","NewTestOwner@mail.ru",nullcontext()),
        ("UnknownTestOwner","123123","NewUnknownTestOwner","NewUnknownTestOwner@mail.ru",pytest.raises(TypeError))
    ])
    def test_update_profile(self,client,name,password,new_name,new_email,expected):
        with client,expected:
            client.post("/auth/login/",data={
                "name":name,
                "password":password
            })
            user = current_user(token=session["auth"])
            client.post(f"/tracker/owner/{user['id']}/profile/",data={
                "name":new_name,
                "email":new_email
            })
            client.get(f"/tracker/worker/{user.get('id')}/profile/")
            new_user = current_user(token=session["auth"])
            assert new_user.get("name") == new_name
            assert new_user.get("email") == new_email


class TestWorker:
    @pytest.mark.parametrize("name,password,expected",[
        ("TestWorker","123123",nullcontext()),
        ("UnknownestWorker","123123",pytest.raises(TypeError))
    ])
    def test_add_project(self,client,name,password,expected):
        with client,expected:
            client.post("/auth/login/",data={
                    "name":name,
                    "password":password
                })
            user = current_user(token=session["auth"])
            
            assert client.post(f"/tracker/worker/{user.get('id')}/create/",data={"title":"test title","description":"test description"}).status_code == 200


    @pytest.mark.parametrize("name,password,new_name,new_email,expected",[
        ("TestWorker","123123","NewTestWorker","NewTestWorker@mail.ru",nullcontext()),
        ("UnknownTestWorker","123123","NewUnknownTestWorker","NewUnknownTestWorker@mail.ru",pytest.raises(TypeError))
    ])
    def test_update_profile(self,client,name,password,new_name,new_email,expected):
        with client,expected:
            client.post("/auth/login/",data={
                "name":name,
                "password":password
            })
            user = current_user(token=session["auth"])
            client.post(f"/tracker/owner/{user['id']}/profile/",data={
                "name":new_name,
                "email":new_email
            })
            client.get(f"/tracker/worker/{user.get('id')}/profile/")
            new_user = current_user(token=session["auth"])
            assert new_user.get("name") == new_name
            assert new_user.get("email") == new_email