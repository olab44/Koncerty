from pydantic import BaseModel
from typing import List


class GroupSchema(BaseModel):
    id: int
    name: str
    extra_info: str | None

    class Config:
        orm_mode = True


class UserGroupsResponse(BaseModel):
    username: str
    groups: List[GroupSchema]
