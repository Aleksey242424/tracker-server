import pytest
from core.auth.schem import User
from contextlib import nullcontext
from tests.cfgtest import *
from flask import session,request
from core.auth.utils import jwt_decode


class TestRegister:
    @pytest.mark.parametrize(
            "user,expected",
            [(User(
                name = "Anton",
               password = "sadjdqweo",
               email = "anton@mail.ru",
               is_owner = True
            ),nullcontext()),
            (User(
                name = "Anton",
               password = "sadjdqweo",
               email = "anton@mail.ru"
            ),pytest.raises(AssertionError)
            )])
    def test_register_auth(self,client,user:User,expected):
        with expected:
            assert client.post("/auth/register/",data={**user.model_dump()}).status_code != 401
    

    def test_token(self,client,user:User = User(
            name="Andrey",
            password = "dasijas",
            email = "andrey@mail.ru",
            is_owner = True
    )):
        with client:
            assert client.post("auth/register/",data={**user.model_dump()}).status_code != 401
            token = session["auth"]
            assert token
            assert jwt_decode(token = token)
            assert jwt_decode(token="invalid.token").status_code == 401


class TestLogin:
    def test_login_auth(self,client,user:User = User(
                name = "Anton",
               password = "sadjdqweo",
            )):
        with client:
            assert client.post("/auth/login/",data={**user.model_dump()}).status_code != 401
            client.get("/auth/login/")
            request.path == "/tracker/owner/"