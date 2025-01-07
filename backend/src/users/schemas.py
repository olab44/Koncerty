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
