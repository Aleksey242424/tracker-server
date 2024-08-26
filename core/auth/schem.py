from pydantic import BaseModel,EmailStr

class User(BaseModel):
    id:int|None = None
    name:str
    password:str
    email:EmailStr|None = None
    is_owner:bool = False