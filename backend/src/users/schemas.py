from pydantic import BaseModel
from typing import List, Optional

class SubgroupSchema(BaseModel):
    subgroup_id: int
    subgroup_name: str
    role: Optional[str]

class GroupSchema(BaseModel):
    group_id: int
    group_name: str
    role: Optional[str]
    subgroups: List[SubgroupSchema]


class UserGroupStructureSchema(BaseModel):
    username: str
    group_structure: List[GroupSchema]

    class Config:
        orm_mode = True