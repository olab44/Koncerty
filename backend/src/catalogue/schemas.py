from pydantic import BaseModel
from typing import List, Optional

class FileInfo(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CompositionInfo(BaseModel):
    id: int
    name: str
    author: str
    files: Optional[List[FileInfo]] = []

    class Config:
        from_attributes = True
    
class CreateCompositionRequest(BaseModel):
    name: str
    author: str
    files: List[int]
    parent_group: int

class FileInfoExtra(BaseModel):
    id: int
    name: str
    access: bool

    class Config:
        from_attributes = True


class CreateCompositionResponse(BaseModel):
    name: str
    author: str
    files: List[FileInfoExtra]

class RemoveCompositionRequest(BaseModel):
    composition_id: int
    parent_group: int
