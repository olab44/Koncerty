from pydantic import BaseModel
from typing import List, Optional

class SubgroupSchema(BaseModel):
    subgroup_id: int
    subgroup_name: str
    extra_info: str

    class Config:
        orm_mode = True

class GroupSchema(BaseModel):
    group_id: int
    group_name: str
    role: Optional[str]
    extra_info: str
    inv_code: Optional[str]
    subgroups: List[SubgroupSchema] = []

    class Config:
        orm_mode = True

class UserGroupStructureSchema(BaseModel):
    username: str
    group_structure: List[GroupSchema]

    class Config:
        orm_mode = True

class CreateGroupRequest(BaseModel):
    parent_group: Optional[int]
    name: str
    extra_info: Optional[str]

class JoinGroupRequest(BaseModel):
    inv_code: str

class CreateSubgroupRequest(BaseModel):
    parent_group: int
    name: str
    extra_info: str
    members: List[int]

class EditGroupRequest(BaseModel):
    group_id: int
    name: str
    extra_info: str
    parent_group: int

class GroupInfo(BaseModel):
    id: int
    parent_group: int
    name: str
    extra_info: str
    inv_code: Optional[str]

class RemoveGroupRequest(BaseModel):
    parent_group: int
    group_id: int

class DeleteGroupResponse(BaseModel):
    id: int
    name: str
    extra_info: str

class AddMemberRequest(BaseModel):
    parent_group: int
    group_id: int
    user_id: int