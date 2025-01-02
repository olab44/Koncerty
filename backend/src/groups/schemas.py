from pydantic import BaseModel

class CreateGroupRequest(BaseModel):
    user_email: str
    parent_group: int
    name: str
    extra_info: str