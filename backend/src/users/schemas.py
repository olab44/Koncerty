from pydantic import BaseModel

class GoogleSignInRequest(BaseModel):
    token: str

class UserCreate(BaseModel):
    username: str