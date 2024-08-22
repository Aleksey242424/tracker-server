from pydantic import BaseModel
from uuid import UUID


class Project(BaseModel):
    id:int|None = None
    token:UUID
    title:str
    description:str
    owner:int|None = None