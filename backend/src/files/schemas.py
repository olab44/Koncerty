from pydantic import BaseModel
from typing import List, Optional


class FileModel(BaseModel):
    id: int
    name: str
    google_drive_id: Optional[str]
    composition_id: Optional[int]

    class Config:
        from_attributes = True


class FileOwnershipModel(BaseModel):
    id: int
    user_id: int
    file_id: int

    class Config:
        from_attributes = True 


class UploadFileRequest(BaseModel):
    file_name: str
    parent_group: int


class DownloadFileRequest(BaseModel):
    file_id: int
    parent_group: int


class DownloadFileResponse(BaseModel):
    downloaded_file: FileModel
    file_path: str

    class Config:
        arbitrary_types_allowed = True


class DeleteFileRequest(BaseModel):
    file_id: int
    parent_group: int


class FileToUserRequest(BaseModel):
    file_id: int
    user_id: int
    parent_group: int


class FileToSubgroupRequest(BaseModel):
    file_id: int
    group_id: int


class FileToCompositionRequest(BaseModel):
    file_id: int
    composition_id: int
    parent_group: int


class DeleteFileToCompositionRequest(BaseModel):
    file_id: int
    parent_group: int

class CompositionSchema(BaseModel):
    composition_id: int
    name: str
    author: str

class FindCompositionResponse(BaseModel):
    found: List[CompositionSchema]

class CreateCompositionRequest(BaseModel):
    name: str
    author: str
    files: List[int]