from pydantic import BaseModel

class CreateGroupRequest(BaseModel):
    token: str
    parent_group: int
    name: str
    extra_info: str