from pydantic import BaseModel
from typing import List, Optional

class SubgroupSchema(BaseModel):
    subgroup_id: int
    subgroup_name: str
    role: Optional[str]
    subgroups: List["SubgroupSchema"] = []  # Rekurencyjne podgrupy

    class Config:
        orm_mode = True

class GroupSchema(BaseModel):
    group_id: int
    group_name: str
    role: Optional[str]
    subgroups: List[SubgroupSchema] = []

    class Config:
        orm_mode = True

class UserGroupStructureSchema(BaseModel):
    username: str
    group_structure: List[GroupSchema]

    class Config:
        orm_mode = True


class GoogleSignInRequest(BaseModel):
    token: str

class UserCreate(BaseModel):
    username: str
    email: str