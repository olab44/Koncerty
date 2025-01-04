from pydantic import BaseModel

class CreateGroupRequest(BaseModel):
    parent_group: int
    name: str
    extra_info: str