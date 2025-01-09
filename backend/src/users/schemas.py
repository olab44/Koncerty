from pydantic import BaseModel
from typing import List

class GoogleSignInRequest(BaseModel):
    token: str

class UserCreate(BaseModel):
    username: str

class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    role: str

class GroupsUserRequest(BaseModel):
    group_id: int

class ChangeUserRoleRequest(BaseModel):
    group_id: int
    user_email: str
    new_role: str

class RemoveMemberRequest(BaseModel):
    group_id: int
    user_email:str
