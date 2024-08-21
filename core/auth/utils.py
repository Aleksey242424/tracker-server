from abc import ABC,abstractmethod
from .schem import User
from bcrypt import gensalt,hashpw
from instance.config import setting
from jwt import encode,decode,ExpiredSignatureError,InvalidSignatureError,DecodeError
from datetime import timedelta,datetime
from flask import abort,Response,make_response,redirect,url_for,session
from core.system_db.crud import PersonCRUD
from functools import wraps


def jwt_encode(
    payload:dict,
    algorithm:str = setting.algorithm,
    private_key:str = setting.private_key.read_text()
):
    payload["sub"] = payload["name"]
    payload["exp"] = datetime.utcnow() + timedelta(seconds=10)
    return encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm
    )


def jwt_decode(
    token:str,
    algorithm:str = setting.algorithm,
    public_key:str = setting.public_key.read_text() 
):
    try:
        return decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm]
        )
    except (InvalidSignatureError,ExpiredSignatureError,DecodeError,ValueError):
        abort(401)


def check_auth(func):
    @wraps(func)
    def decorator(*a,**kw):
        if session.get("auth"):
            return redirect(url_for("tracker.main"))
        return func(*a,**kw)
    return decorator


class BaseAuth(ABC):
    def __init__(self,form_data:dict):
        self.user = self.init_user(form_data=form_data)
        self.hash_password = self.generate_hash_password(self.user.password.encode("utf-8")).decode("utf-8")
        self.person_crud = PersonCRUD

    def generate_hash_password(self,password:str,salt = gensalt()) -> bytes:
        return hashpw(
            password=password,
            salt=salt
            )
    
    def init_user(self,form_data:dict) -> User:
        try:
            form_data.__delitem__("csrf_token")
            form_data.__delitem__("confirm_password")

            if self.__class__.__name__ == "RegisterAuth":
                form_data.__delitem__("sign_up")

            else:
                form_data.__delitem__("sign_in")

        except KeyError:
            pass

        finally:
            return User(**form_data)

    @abstractmethod
    def main(self):
        ...

    def init_response(self,token:str):
        session["auth"] = token
        response = make_response(
            redirect(
                url_for("tracker.main")
            )
        )
        response.headers["Authorization"] = f"Bearer {token}"
        return response
    

class RegisterAuth(BaseAuth):

    def main(self) -> Response:
        self.person_crud.add(
            name=self.user.name,
            hash_password=self.hash_password,
            email = self.user.email,
            is_owner=self.user.is_owner
        )

        token = jwt_encode(
            payload=self.user.model_dump()
        )

        return self.init_response(token=token)

        

class LoginAuth(BaseAuth):
    def main(self) -> Response:
        user_data = self.person_crud.get(
            name=self.user.name,
            password=self.user.password
        )

        if not user_data:
            abort(401)

        user = self.init_user(
            form_data={
                "name":user_data[0],
                "password":self.user.password,
                "email":user_data[2],
                "is_owner":user_data[3]
            }
        )

        token = jwt_encode(
            payload = user.model_dump()
        )
        return self.init_response(
            token=token
        )
    

