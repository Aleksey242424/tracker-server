from pydantic import BaseModel
from pydantic_settings import BaseSettings,SettingsConfigDict
from os import urandom
from pathlib import Path

class Token(BaseModel):
    algorithm:str = "RS256"
    path_to_certs:Path = Path("instance/certs")
    private_key:Path = path_to_certs / "private.pem"
    public_key:Path = path_to_certs / "public.pem"


class DB(BaseModel):
    DB_DIALECT:str
    DB_USER:str
    DB_PASSWORD:str
    DB_PORT:int
    DB_HOST:str
    DB_NAME:str

    @property
    def DB_CONNECTION(self) -> str:
        return f"{self.DB_DIALECT}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class Setting(DB,Token,BaseSettings):
    SECRET_KEY:bytes = urandom(20)
    model_config = SettingsConfigDict(env_file="instance/.env")


setting = Setting()