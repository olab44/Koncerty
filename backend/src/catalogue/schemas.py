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
