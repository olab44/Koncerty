from pydantic import BaseModel
from typing import List, Optional

class GoogleSignInRequest(BaseModel):
    token: str

class UserCreate(BaseModel):
    username: str

class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    role: Optional[str]

class GroupsUserRequest(BaseModel):
    group_id: int

class ChangeUserRoleRequest(BaseModel):
    group_id: int
    user_email: str
    new_role: str
    parent_group: int

class RemoveMemberRequest(BaseModel):
    group_id: int
    user_email:str
    parent_group: int
