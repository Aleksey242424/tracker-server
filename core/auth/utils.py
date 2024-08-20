from abc import ABC,abstractmethod
from .schem import User
from bcrypt import gensalt,hashpw
from instance.config import setting
from jwt import encode,decode,ExpiredSignatureError
from datetime import timedelta,datetime
from flask import abort,Response,make_response,redirect,url_for,session
from core.system_db.crud import PersonCRUD


def jwt_encode(
    payload:dict,
    algorithm:str = setting.algorithm,
    private_key:str = setting.private_key.read_text()
):
    payload["sub"] = payload["name"]
    payload["exp"] = datetime.utcnow() + timedelta(minutes=1)
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
    except ExpiredSignatureError:
        abort(Response(
            status=401,
            headers={"WWW-Authenticated":"Bearer"}
        ))
    


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
    @abstractmethod
    def init_user(self,form_data:dict) -> User:
        ...

    @abstractmethod
    def main(self,*a,**kw):
        ...

    def init_response(self,token):
        session["auth"] = token
        response = make_response(
            redirect(
                url_for("tracker.main")
            )
        )
        response.headers["Authorization"] = f"Bearer {token}"
        return response
    

class RegisterAuth(BaseAuth):

    def main(self):
        self.person_crud.add(
            name=self.user.name,
            hash_password=self.hash_password,
            email = self.user.email,
            is_owner=self.user.is_owner
        )

        token = jwt_encode(
            payload=self.user.dict()
        )

        return self.init_response(token=token)
    

    def init_user(self,form_data:dict) -> User:
        try:
            form_data.__delitem__("csrf_token")
            form_data.__delitem__("confirm_password")
            form_data.__delitem__("sign_up")

        except KeyError:
            pass

        finally:
            return User(**form_data)